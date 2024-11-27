import argparse
import os
import subprocess
from typing import List, Dict


def _read_arguments():
    parser = argparse.ArgumentParser(description='The script to download audio tracks (webm) from YouTube playlist')
    parser.add_argument("path",
                        help="Path to the local directory where the webm files are, or a single webm file.")
    parser.add_argument("--ffmpeg-exe",
                        help="Path to mp3gain.exe, including file name (PATH variable is used otherwise).")
    ret = parser.parse_args()
    return ret


def convert_webm_folder_to_mp3(ffmpeg_exe: str, folder: str):
    webm_files = [f for f in os.listdir(folder) if os.path.isfile(f) and len(f) > 5 and f[-5:].lower() == ".webm"]
    for webm_file in webm_files:
        convert_webm_file_to_mp3(ffmpeg_exe, webm_file)


def convert_webm_files_to_mp3(ffmpeg_exe: str, lst: List[Dict]):
    '''

    :param ffmpeg_exe: full path to ffmpeg_exe file
    :param lst: List of dicts. Must contain file_name:string/title:string/abr:int
    :return: None
    '''

    for item in lst:
        convert_webm_file_to_mp3(ffmpeg_exe, item["file"], title=item["title"], abr=item["abr"])


def convert_webm_file_to_mp3(ffmpeg_exe: str, file_name: str, title: str = None, abr: int = None) -> None:
    if title is None:
        title = file_name
    try:
        print(f"{title} webm => mp3")
        in_file = file_name
        out_file = file_name[:-4] + ".mp3"
        params = [ffmpeg_exe, "-i", in_file, "-vn"]
        if abr is not None:
            params.extend(["-ab", str(abr) + "k"])
        params.extend(["-loglevel", "warning", "-y", out_file])
        res = subprocess.run(params)
        if res.returncode == 0:
            os.remove(in_file)
    except Exception as e:
        print(f"Failed to convert {title}. Error: {str(e)}. Skipped.")


def main():
    args = _read_arguments()
    print(f"webm => mp3 for '{args.path}'")
    if os.path.isfile(args.path):
        convert_webm_file_to_mp3(args.ffmpeg_exe, args.path)
    else:
        convert_webm_folder_to_mp3(args.ffmpeg_exe, args.path)


if __name__ == "__main__":
    main()
