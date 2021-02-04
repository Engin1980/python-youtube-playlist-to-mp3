import argparse
import os
import subprocess
from typing import List


def _read_arguments():
    parser = argparse.ArgumentParser(description='The script to download audio tracks (webm) from YouTube playlist')
    parser.add_argument("path",
                        help="Path to the local directory where the mp3 files are, or a single MP3 file.")
    parser.add_argument("--mp3gain-exe",
                        help="Path to mp3gain.exe, including file name (PATH variable is used otherwise).",
                        default="mp3gain.exe")
    parser.add_argument("--target-gain",
                        help="Value of target gain. Default is 89.",
                        default=89)
    ret = parser.parse_args()
    return ret


def process_folder(mp3gain_exe: str, folder: str, target_gain: int = 89) -> None:
    mp3files = [f for f in os.listdir(folder) if os.path.isfile(f) and len(f) > 4 and f[-4:].lower() == ".mp3"]
    print(f"\tfound {len(mp3files)} files")
    tmp = [os.path.join(folder, q) for q in mp3files]
    process_files(mp3gain_exe, tmp, target_gain=target_gain)


def process_files(mp3gain_exe: str, mp3files: List[str], target_gain: int = 89) -> None:
    for mp3file in mp3files:
        process_file(mp3file, mp3gain_exe, target_gain=target_gain)


def process_file(mp3gain_exe: str, mp3file: str, target_gain: int = 89) -> None:
    print(f"mp3gain => {mp3file}")
    try:
        params = [mp3gain_exe, "-r"]
        if target_gain != 89:
            addiction = target_gain - 89
            addiction = float(addiction)
            params.append("-d")
            params.append(str(addiction))
        params.append(mp3file)
        subprocess.run(params)
    except Exception as e:
        print(f"Failed to apply mp3gain on '{mp3file}'. Error: " + str(e) + ".")


def main():
    args = _read_arguments()
    print(f"MP3Gain for '{args.path}'")
    if os.path.isfile(args.path):
        process_file(args.mp3gain_exe, args.path, args.target_gain)
    else:
        process_folder(args.mp3gain_exe, args.path, args.target_gain)


if __name__ == "__main__":
    main()
