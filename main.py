import argparse
import os
import json
from dataclasses import dataclass

from lib import mp3gain, webm2mp3, track_history
from lib.pytubefix_downloader import download, PlaylistDownloadType


@dataclass
class Config:
    mp3gain_exe: str
    ffmpeg_exe: str


def __read_arguments():
    parser = argparse.ArgumentParser(description='The script to download audio tracks (webm) from YouTube playlist')
    parser.add_argument("url",
                        help="URL of YouTube playlist. Mandatory.")
    parser.add_argument("output_path", metavar="output-path",
                        help="Path to the local directory where the result will be saved. Mandatory.")
    parser.add_argument("--long-playlist-support-enabled",
                        help="Use for playlists longer than 100 tracks. Optional, default false.",
                        default=False)
    parser.add_argument("--dont-load-history",
                        help="Do not load the history file from previous downloading.",
                        action="store_true")
    parser.add_argument("--dont-save-history",
                        help="Do not save the history file after current downloading",
                        action="store_true")
    parser.add_argument("--delay",
                        help="Delay between downloads (in seconds). Optional, default 10.",
                        type=int,
                        default=10)
    parser.add_argument("--history-filename",
                        help="Name of the file where download history is stored. Optional."
                             " Default: __downloaded.yt.json",
                        default=track_history.DEFAULT_HISTORY_FILE_NAME)
    parser.add_argument("--to-mp3",
                        help="Convert downloaded *.webm files to *.mp3 files and delete *.webm files.",
                        action="store_true")
    parser.add_argument("--adjust-mp3-gain",
                        help="Adjust track gain. Only applicable if --to-mp3 is used.",
                        action="store_true")
    parser.add_argument("--target-mp3-gain",
                        help="Sets the target mp3 gain. Only applicable if --adjust-mp3-gain is used. "
                             "Default value is 89.",
                        type=int,
                        default=89)
    parser.add_argument("--repeat-errors",
                        help="If used, previously failed downloads are repeated.",
                        action="store_true")
    ret = parser.parse_args()
    return ret


def __load_history(args):
    full_history_file_name = os.path.join(args.output_path, args.history_filename)
    ret = track_history.try_load_track_history(full_history_file_name)
    return ret


def __save_history(args, history):
    if args.dont_save_history:
        return
    else:
        full_history_file_name = os.path.join(args.output_path, args.history_filename)
        track_history.save_track_history(history, full_history_file_name)


def __merge_history(old, new):
    ret = {}
    for key in old:
        ret[key] = old[key]
    for key in new:
        ret[key] = new[key]
    return ret


def __print_environment():
    print("Current interpreter:")
    import sys
    print(sys.executable)

    print("Current environment")
    import importlib_metadata
    dists = importlib_metadata.distributions()
    for dist in dists:
        name = dist.metadata["Name"]
        version = dist.version
        print(f'\t{name}=={version}')
    print()


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

    return ret


def __print_configuration(cfg:Config):
    print("Configuration:")
    print(f"\tmp3gain_exe: {cfg.mp3gain_exe}")
    print(f"\tffmpeg_exe: {cfg.ffmpeg_exe}")
    print()


def __print_arguments(args):
    print("Arguments:")
    print(f"\turl: {args.url}")
    print(f"\toutput_path: {args.output_path}")
    print(f"\tlong_playlist_support_enabled: {args.long_playlist_support_enabled}")
    print(f"\tdont_load_history: {args.dont_load_history}")
    print(f"\tdont_save_history: {args.dont_save_history}")
    print(f"\tdelay: {args.delay}")
    print(f"\thistory_filename: {args.history_filename}")
    print(f"\tto_mp3: {args.to_mp3}")
    print(f"\tadjust_mp3_gain: {args.adjust_mp3_gain}")
    print(f"\ttarget_mp3_gain: {args.target_mp3_gain}")
    print(f"\trepeat_errors: {args.repeat_errors}")
    print()


def main():
    args = __read_arguments()
    __print_environment()

    cfg = __load_config()
    __print_configuration(cfg)

    __print_arguments(args)

    pds: PlaylistDownloadType = PlaylistDownloadType.SELENIUM \
        if args.long_playlist_support_enabled \
        else PlaylistDownloadType.PYTUBEFIX

    history_old = {} if args.dont_load_history else __load_history(args)
    history_new = download(args.url, pds, args.output_path, history_old,
                           delay_between_tracks=args.delay, repeat_errors=args.repeat_errors,
                           verbose=True)

    if args.to_mp3:
        tmp = [h for h in history_new.values() if h.status == "downloaded"]
        tmp = [{"file": h.target_file, "title": h.title, "abr": h.abr} for h in tmp]
        webm2mp3.convert_webm_files_to_mp3(args.ffmpeg_exe, tmp)

        if args.adjust_mp3_gain:
            files = [q["file"] for q in tmp]
            files = [file[:-4] + ".mp3" for file in files]
            mp3gain.process_files(args.mp3gain_exe, files, args.target_mp3_gain)

    history = __merge_history(history_old, history_new)
    if not args.dont_save_history:
        __save_history(args, history)


if __name__ == "__main__":
    main()
