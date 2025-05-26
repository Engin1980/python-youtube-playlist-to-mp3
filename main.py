import argparse
import os

from lib import mp3gain, webm2mp3, track_history
from downloader import download


def _read_arguments():
    parser = argparse.ArgumentParser(description='The script to download audio tracks (webm) from YouTube playlist')
    parser.add_argument("url",
                        help="URL of YouTube playlist. Mandatory.")
    parser.add_argument("--local-file",
                        help="Path to the local file where the list of YouTube URLs is stored in HTML. Optional.")
    parser.add_argument("output_path", metavar="output-path",
                        help="Path to the local directory where the result will be saved. Mandatory.")
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
    parser.add_argument("--ffmpeg-exe",
                        help="Path to ffmpeg.exe, including file name (PATH variable is used otherwise).",
                        default="ffmpeg.exe")
    parser.add_argument("--adjust-mp3-gain",
                        help="Adjust track gain. Only applicable if --to-mp3 is used.",
                        action="store_true")
    parser.add_argument("--target-mp3-gain",
                        help="Sets the target mp3 gain. Only applicable if --adjust-mp3-gain is used. "
                             "Default value is 89.",
                        type=int,
                        default=89)
    parser.add_argument("--mp3gain-exe",
                        help="Path to mp3gain.exe, including file name (PATH variable is used otherwise).",
                        default="mp3gain.exe")
    parser.add_argument("--repeat-errors",
                        help="If used, previously failed downloads are repeated.",
                        action="store_true")
    ret = parser.parse_args()
    return ret


def _load_history(args):
    full_history_file_name = os.path.join(args.output_path, args.history_filename)
    ret = track_history.try_load_track_history(full_history_file_name)
    return ret


def _save_history(args, history):
    if args.dont_save_history:
        return
    else:
        full_history_file_name = os.path.join(args.output_path, args.history_filename)
        track_history.save_track_history(history, full_history_file_name)


def _merge_history(old, new):
    ret = {}
    for key in old:
        ret[key] = old[key]
    for key in new:
        ret[key] = new[key]
    return ret


def print_environment():
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


def main():
    args = _read_arguments()
    print_environment()
    history_old = {} if args.dont_load_history else _load_history(args)
    history_new = download(args.url, args.output_path, history_old,
                           delay_between_tracks=args.delay, repeat_errors=args.repeat_errors,
                           local_file=args.local_file,
                           verbose=True)

    if args.to_mp3:
        tmp = [h for h in history_new.values() if h.status == "downloaded"]
        tmp = [{"file": h.target_file, "title": h.title, "abr": h.abr} for h in tmp]
        webm2mp3.convert_webm_files_to_mp3(args.ffmpeg_exe, tmp)
        if args.adjust_mp3_gain:
            files = [q["file"] for q in tmp]
            files = [file[:-4] + ".mp3" for file in files]
            mp3gain.process_files(args.mp3gain_exe, files, args.target_mp3_gain)

    history = _merge_history(history_old, history_new)
    if not args.dont_save_history:
        _save_history(args, history)


if __name__ == "__main__":
    main()
