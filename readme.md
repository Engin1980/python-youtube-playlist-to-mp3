# (Python) YouTube Playlist To MP3

## Description

This repository contains a simple script(s) to download YouTube playlist
(represented as URL) into a set of `*.webm` files, which can be later converted
into the `*.mp3` audio files. The script stores the processed playlist items, so 
they are skipped next time the script is executed.

The script supports only audio stream downloading. However, feel free to adjust 
the code for the video support.

The conversion to `*.mp3` needs an instalation of FFMPEG to be available on 
the target computer.

### Main features:
* Analyse tracks in the YouTube playlist
* From every track, download best audio (highest bit-rate) stream to local drive as `*.webm` file
* Skips missing/failed tracks
* (Optionally) Skips tracks downloaded in previous execution(s)
* (Optionally) Convert tracks from `*.webm` to `*.mp3` format

## Requirements & Installation

The script was tested on Python 3.7.6. 

Additional required libraries are presented in `requirements.txt` file in the 
repository.

To convert `*.webm` files to `*.mp3` files FFMPEG is required.

### Instalation
1. Ensure you have, or install [Python 3.x.x](https://www.python.org/downloads/).
2. [To convert files to MP3] Ensure you have, or download and extract/install [FFMPEG](https://ffmpeg.org/download.html).
3. Start Terminal/Command line/Powershell and enter the following command sequence:
    
   3.1 Download or clone this repository (only files from the root are required).

   3.2 (Optionally, but suggested) Create [new virtual environment](https://docs.python.org/3/library/venv.html) 
   to be used with this repository.
   
   3.3 [Install the required packages](https://pip.pypa.io/en/stable/reference/pip_install/) 
   from requirements file `requirements.txt`.
   
## Execution

The execution is done via `main.py` script. From command line/terminal, the generic usage
is:
```shell
main.py [-h] [--dont-load-history] [--dont-save-history]
               [--delay DELAY] [--history-filename HISTORY_FILENAME]
               [--to-mp3] [--ffmpeg-path FFMPEG_PATH]
               url output-path
```

Simple usage from command line:
```shell
python main.py https://www.youtube.com/playlist?list=ACF5.... C:/TEMP
```

There are command line arguments available (note `url` and `output-path` are mandatory positional arguments):


| Parameter | Meaning | Mand./Def. |
| --------- | ------- | ---------- |
| url       | The URL of the input YouTube playlist, e.g. `https://www.youtube.com/playlist?list=OLAK5...` | (Must be provided.) |
| output&#8209;path | The output path (absolute or relative) where the result will be stored. | (Must be provided.) |
| &#8209;&#8209;dont&#8209;load&#8209;history | If set, the previously downloaded tracks will be downloaded again. | History loaded by default |
| &#8209;&#8209;dont&#8209;save&#8209;history | If set, the list of downloaded tracks will not be saved for future history use. | History saved by default |
| &#8209;&#8209;history&#8209;filename | Sets the custom history filename, if required. May be absolute or relative. If relative, the file is stored in the output path. | If not set, default name is used. |
| &#8209;&#8209;delay | Sets the gap (sleep interval) in seconds between download end/start (to not overhaul YouTube server). | Default value is 10 |
| &#8209;&#8209;to&#8209;mp3 | If set, the program will convert downloaded `*.webm` files into `*.mp3` files using FFMPEG. If the conversion is successful, the `*.webm` files are deleted. | Conversion is not done by default. |
| &#8209;&#8209;ffmpeg&#8209;path | Location (absolute or relative) to `ffmpeg.exe` file. If not set, the `PATH` environment variable is used to detect the file location. If the file is not found, the script will crash. | Use `PATH` environment variable by default.

More complex usage:

```shell
python main.py --dont-load-hstory --delay 10 --to-mp3 --ffmpeg-path "c:/program files/ffmpeg/ffmpeg.exe" https://www.youtube.com/playlist?list=ACF5... C:/TEMP
```

   

