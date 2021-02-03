import argparse
import os
import subprocess

import track_history
from downloader import download


def _read_arguments():
    parser = argparse.ArgumentParser(description='The script to download audio tracks (webm) from YouTube playlist')
    parser.add_argument("url",
                        help="URL of YouTube playlist. Mandatory.")
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
    parser.add_argument("--ffmpeg-path",
                        help="Path to ffmpeg.exe (PATH variable is used otherwise).")
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


def _convert_files_to_mp3(args, history):
    ffmpeg_exe = "ffmpeg.exe" if args.ffmpeg_path is None else args.ffmpeg_path
    for key in history.keys():
        item = history[key]
        if item.status != "downloaded": continue

        try:
            _convert_file_to_mp3(ffmpeg_exe, item)
        except Exception as e:
            print(f"Failed to convert {item.title}. Error: {str(e)}. Skipped.")


def _convert_file_to_mp3(ffmpeg_exe, item):
    print(f"{item.title} webm => mp3")
    in_file = item.target_file
    out_file = item.target_file[:-5] + ".mp3"
    res = subprocess.run(
        [ffmpeg_exe, "-i", in_file, "-vn", "-ab", str(item.abr) + "k", "-loglevel", "warning", "-y", out_file])
    if res.returncode == 0:
        os.remove(in_file)


def main():
    args = _read_arguments()
    history_old = {} if args.dont_load_history else _load_history(args)
    history_new = download(args.url, args.output_path, history_old, delay_between_tracks=args.delay, verbose=True)

    if args.to_mp3:
        _convert_files_to_mp3(args, history_new)

    history = _merge_history(history_old, history_new)
    if not args.dont_save_history:
        _save_history(args, history)


if __name__ == "__main__":
    main()
