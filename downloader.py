import datetime
import time
from typing import Dict

from pytube import Playlist, YouTube

from track_history import TrackHistory

_verbose = True


def _log(*args, **kwargs):
    if (_verbose):
        print(*args, **kwargs)


def download(
        url: str, output: str, history_old: Dict[str, TrackHistory], *,
        delay_between_tracks: int = 10, verbose: bool = True) -> Dict[str, TrackHistory]:
    global _verbose
    _verbose = verbose
    history_new = {}
    _log("Fetching playlist...")
    ypl = Playlist(url)
    track_count = len(ypl.video_urls)
    _log(f"Found playlist '{ypl.title}' with {track_count} tracks, {len(history_old)} seems to be downloaded already.")
    _log("Going for videos...")
    for index, url in enumerate(ypl.video_urls):
        _log(f"{index + 1}. of {track_count}")
        if url in history_old.keys():
            _log(f"\tVideo '{history_old[url].title}' already processed as '{history_old[url].status}', skipping")
            continue
        try:
            yt = YouTube(url)
            try:
                (out_file_name, stream_id, abr) = _process_video(yt, output)
                history_new[url] = _create_history_record_success(yt, stream_id, abr, out_file_name)
            except Exception as e:
                _log("\tVideo " + str(index) + " :: " + url + " erroneous, will be not downloaded: " + e.__str__())
                history_new[url] = _create_history_record_fail("Error when downloading stream.", e, yt=yt)
        except Exception as e:
            _log("\tVideo " + str(index) + " :: " + url + " erroneous, will be not downloaded: " + e.__str__())
            history_new[url] = _create_history_record_fail("Unable to fetch from YouTube", e, yt=None)

        _log("\tAnti-block-delay...")
        time.sleep(delay_between_tracks)
        _log("\t\t... resuming")

    return history_new


def _process_video(yt, output_path):
    _log(f"\ttitle: {yt.title}")
    _log(f"\tlength: {yt.length} seconds")
    ys, abr = _get_best_audio_stream(yt)
    _log("\t\tAudio stream: ", ys)
    _log("\tDownloading...")
    final_file_name = ys.download(output_path=output_path)
    _log("\t... completed")
    return final_file_name, ys.itag, abr


def _get_best_audio_stream(yt):
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


def _create_history_record_success(yt, stream_id, abr, output_file_name):
    track = TrackHistory()
    track.title = yt.title
    track.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    track.stream_id = stream_id
    track.abr = abr
    track.target_file = output_file_name
    track.status = "downloaded"

    return track


def _create_history_record_fail(error_info, exception, yt=None):
    track = TrackHistory()
    track.title = None if yt is None else yt.title
    track.date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    track.stream_id = None
    track.target_file = None
    track.status = "error: " + error_info + " :: " + str(exception)

    return track
