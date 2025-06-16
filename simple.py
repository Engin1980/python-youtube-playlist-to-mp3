import json
import os
from dataclasses import dataclass
from typing import Dict

from lib import webm2mp3
from lib.pytubefix_downloader import download_list, download_video, PlaylistDownloadType
from lib.track_history import TrackHistory


@dataclass
class Config:
    mp3gain_exe: str
    ffmpeg_exe: str
    delay_between_downloads: int
    verbose: bool


def __load_config():
    if not os.path.exists("config.json"):
        raise FileNotFoundError("Configuration file 'config.json' not found. "
                                "Please create it with the required settings.")

    with open("config.json") as f:
        data = json.load(f)

    ret: Config = Config(**data)

    if not os.path.exists(ret.mp3gain_exe):
        raise FileNotFoundError(f"mp3gain executable not found: {ret.mp3gain_exe} ({os.path.abspath(ret.mp3gain_exe)})")
    if not os.path.exists(ret.ffmpeg_exe):
        raise FileNotFoundError(f"ffmpeg executable not found: {ret.ffmpeg_exe} ({os.path.abspath(ret.ffmpeg_exe)})")
    if ret.delay_between_downloads < 0:
        raise ValueError(f"Invalid delay value: {ret.delay_between_downloads}. "
                         "It must be a non-negative integer.")

    return ret


def main():
    print("* * * Simple YouTube -> audio download * * *")
    print("This is a simple tool to download YouTube video/playlist to audio files.")
    print("It is only for demonstration purposes. "
          "For more detailed specification see the documentation and use 'main.py' file."
          "Note the max length of playlist in this simple demo is 99 files. For longer playlists "
          "you have to use the full version.")

    url: str = input("Enter the URL of YouTube video/playlist: ")
    is_playlist: bool = "list=?" in url

    out_path: str = input("Enter the output directory (should be existing and empty): ")
    if os.path.exists(out_path) is False or os.path.isdir(out_path) is False:
        print(f"The path '{os.path.abspath(out_path)}' does not exist or is not a directory. Exiting.")
        return

    tmp = input(
        "Convert .m4a output to MP3 (note you need to have ffmpeg installed and set up in config file) - Y/n: ")
    to_mp3: bool = tmp.strip().lower() == "y"
    del tmp

    try:
        cfg = __load_config()
    except Exception as ex:
        print(f"Failed to read configuration file. Exiting. More detailed reason: {ex}")
        return

    history_new: Dict[str, TrackHistory]
    if is_playlist:
        history_new = download_list(
            url,
            PlaylistDownloadType.PYTUBEFIX,
            out_path, {})
    else:
        history_new = download_video(url, out_path)

    if to_mp3:
        tmp = [h for h in history_new.values() if h.status == "downloaded"]
        tmp = [{"file": h.target_file, "title": h.title, "abr": h.abr} for h in tmp]
        webm2mp3.convert_webm_files_to_mp3(cfg.ffmpeg_exe, tmp)

    print("Completed")


if __name__ == "__main__":
    main()
