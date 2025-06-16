import datetime
import re
import time
from enum import Enum
from typing import Dict
from typing import List

# from pytube import Playlist, YouTube
from pytubefix import Playlist, YouTube

import lib.selenium_playlist_html_downloader as selenium_downloader
from lib.track_history import TrackHistory

__verbose = True


class PlaylistDownloadType(Enum):
    PYTUBEFIX = 1,
    SELENIUM = 2


def __log(*args, **kwargs):
    if __verbose:
        print(*args, **kwargs)


def __get_tracks_using_pytubefix(url: str):
    __log("Fetching playlist...")
    ret: List[str] = []
    try:
        ypl = Playlist(url)
        for url in ypl.video_urls:
            ret.append(url)
    except Exception as ex:
        __log(f"ERROR: Failed to download the playlist. Check it is NOT PRIVATE.")
        raise (ex)
    return ret


def __get_tracks_using_selenium(url: str):
    __log("Fetching YouTube video from local file...")
    ret: List[str] = []
    html_content = selenium_downloader.download_playlist_html(url, verbose=__verbose)
    regex = r"<a id=\"video-title\" class=\"yt-simple-endpoint style-scope ytd-playlist-video-renderer\" title=\"(.+)\" href=\"(.+?)&.+\">"
    matches = re.findall(regex, html_content)
    for match in matches:
        url = "https://www.youtube.com" + match[1]
        ret.append(url)
    return ret


def download_video(
        url: str, output: str, history_old: Dict[str, TrackHistory] | None = None, repeat_errors: bool = False,
        verbose=True) -> Dict[str, TrackHistory]:
    global __verbose
    __verbose = verbose
    history_new = {}
    track_urls: List[str]

    if history_old is None:
        history_old = {}

    if url in history_old.keys():
        if repeat_errors and history_old[url].status.startswith("error:"):
            __log(
                f"\tVideo '{history_old[url].title}' already processed as '{history_old[url].status}' with an error, we will give it another try")
        else:
            __log(f"\tVideo '{history_old[url].title}' already processed as '{history_old[url].status}', skipping")
            return history_old

    try:
        yt = YouTube(url)
        try:
            (out_file_name, stream_id, abr) = __process_video(yt, output)
            history_new[url] = __create_history_record_success(yt, stream_id, abr, out_file_name)
        except Exception as e:
            __log("\tVideo " + url + " erroneous, will be not downloaded: " + e.__str__())
            history_new[url] = __create_history_record_fail("Error when downloading stream.", e, yt=yt)
    except Exception as e:
        __log("\tVideo " + url + " erroneous, will be not downloaded: " + e.__str__())
        history_new[url] = __create_history_record_fail("Unable to fetch from YouTube", e, yt=None)

    return history_new


def download_list(
        url: str, playlist_download_type: PlaylistDownloadType, output: str, history_old: Dict[str, TrackHistory], *,
        delay_between_tracks: int = 10, repeat_errors: bool = False,
        verbose: bool = True) -> Dict[str, TrackHistory]:
    global __verbose
    __verbose = verbose
    history_new = {}
    track_urls: List[str]

    if playlist_download_type == PlaylistDownloadType.PYTUBEFIX:
        track_urls = __get_tracks_using_pytubefix(url)
    elif playlist_download_type == PlaylistDownloadType.SELENIUM:
        track_urls = __get_tracks_using_selenium(url)
    else:
        raise ValueError(f"Unknown playlist download type: {playlist_download_type}")

    __log(f"Found playlist with {len(track_urls)} tracks, {len(history_old)} seems to be downloaded already.")
    __log("Looking for videos...")
    track_count = len(track_urls)
    for index, url in enumerate(track_urls):
        __log(f"{index + 1}. of {track_count}")
        if url in history_old.keys():
            if repeat_errors and history_old[url].status.startswith("error:"):
                __log(
                    f"\tVideo '{history_old[url].title}' already processed as '{history_old[url].status}' with an error, we will give it another try")
            else:
                __log(f"\tVideo '{history_old[url].title}' already processed as '{history_old[url].status}', skipping")
                continue
        try:
            yt = YouTube(url)
            try:
                (out_file_name, stream_id, abr) = __process_video(yt, output)
                history_new[url] = __create_history_record_success(yt, stream_id, abr, out_file_name)
            except Exception as e:
                __log("\tVideo " + str(index) + " :: " + url + " erroneous, will be not downloaded: " + e.__str__())
                history_new[url] = __create_history_record_fail("Error when downloading stream.", e, yt=yt)
        except Exception as e:
            __log("\tVideo " + str(index) + " :: " + url + " erroneous, will be not downloaded: " + e.__str__())
            history_new[url] = __create_history_record_fail("Unable to fetch from YouTube", e, yt=None)

        __log("\tAnti-block-delay...")
        time.sleep(delay_between_tracks)
        __log("\t\t... resuming")

    return history_new


def __convert_to_valid_filename(s: str, replacement: str = "_", max_length: int = 255) -> str:
    s = re.sub(r'[<>:"/\\|?*\x00-\x1F]', replacement, s)
    s = s.strip().strip(".")
    s = re.sub(f"{re.escape(replacement)}+", replacement, s)
    s = s[:max_length]
    return s


def __process_video(yt, output_path):
    __log(f"\ttitle: {yt.title}")
    __log(f"\tlength: {yt.length} seconds")

    author = yt.author

    ys, abr = __get_best_audio_stream(yt)
    __log("\t\tAudio stream: ", ys)
    __log("\tDownloading...")
    final_file_name = ys.download(output_path=output_path)
    __log("\t... completed")

    def __extend_file_name_if_required(file_path: str, prefix: str) -> str:
        import os
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        if "-" in filename:
            return file_path

        new_file_path = os.path.join(directory, prefix + " -- " + filename)
        os.rename(file_path, new_file_path)
        return new_file_path

    final_file_name = __extend_file_name_if_required(final_file_name, author)

    return final_file_name, ys.itag, abr


def __get_best_audio_stream(yt):
    ret = None
    best_abr = 0
    for stream in yt.streams:
        if stream.mime_type != "audio/webm":
            continue
        curr_abr = int(stream.abr[:-4])
        if curr_abr > best_abr:
            ret = stream
            best_abr = curr_abr
    return ret, best_abr


def __create_history_record_success(yt, stream_id, abr, output_file_name):
    track = TrackHistory()
    track.title = yt.title
    track.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    track.stream_id = stream_id
    track.abr = abr
    track.target_file = output_file_name
    track.status = "downloaded"

    return track


def __create_history_record_fail(error_info, exception, yt=None):
    track = TrackHistory()
    track.title = None if yt is None else yt.title
    track.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    track.stream_id = None
    track.target_file = None
    track.status = "error: " + error_info + " :: " + str(exception)

    return track
