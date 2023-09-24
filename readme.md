# (Python) YouTube Playlist To MP3

## Description

This repository contains a simple script(s) to download YouTube playlist
(represented as URL) into a set of `*.webm` files, which can be later converted
into the `*.mp3` audio files and their volume can be adjusted. The script stores the processed playlist items, so 
they are skipped next time the script is executed.

The script supports only audio stream downloading. However, feel free to adjust 
the code for the video support.

The conversion to `*.mp3` needs an instalation of FFMPEG to be available on 
the target computer. To adjust `.mp3` volume, MP3_GAIN must be available on the target computer (Windows OS only).

### Main features:
* Analyse tracks in the YouTube playlist
* From every track, download the best audio (highest bit-rate) stream to local drive as `*.webm` file
* Skips missing/failed tracks
* (Optionally) Skips tracks downloaded in previous execution(s)
* (Optionally) Convert tracks from `*.webm` to `*.mp3` format
* (Optionally, Windows OS only) Adjusts mp3 volume

![Activity sequence](docs/activity.png)

## History

| Date | Note                                                                                      |
| --- |-------------------------------------------------------------------------------------------|
| 2023-09-24 | Updated version of pytube to 15.0.0 and other dependent packages (see `requirements.txt`) | 
| 2021-05-26 | Updated version of pytube [__downloaded.yt.json](..%2F..%2F..%2FOneDrive%20-%20Ostravska%20univerzita%2FSynchronized%2FYouTube%20Playlists%2FETrance%2F__downloaded.yt.json)to 10.8.2 (older invokes error 404)                             |
| 2021-04-02 | Updated version of pytube to 10.6.1 (older invokes error 410)                             |
| 2021-02-10 | First published working version                                                           |


## Requirements & Installation

The script was tested on Python 3.7.6. 

Additional required libraries are presented in `requirements.txt` file in the 
repository.

To convert `*.webm` files to `*.mp3` files FFMPEG is required.

To adjust volume of MP3 files, the command line version of _MP3 Gain_ must be installed.

### Instalation
1. Ensure you have, or install [Python 3.x.x](https://www.python.org/downloads/).
2. [To convert files to MP3] Ensure you have, or download and extract/install [FFMPEG](https://ffmpeg.org/download.html).
3. [To adjust MP3 file volume] Ensure you have, or download and extract/install [MP3_GAIN](http://mp3gain.sourceforge.net/) (command line version is sufficient).   
4. Start Terminal/Command line/Powershell and enter the following command sequence:
    
   4.1 Download or clone this repository (only files from the root are required).

   4.2 (Optionally, but suggested) Create [new virtual environment](https://docs.python.org/3/library/venv.html) 
   to be used with this repository.
   
   4.3 [Install the required packages](https://pip.pypa.io/en/stable/reference/pip_install/) 
   from requirements file `requirements.txt`.
   
## Execution

The execution is done via `main.py` script. From command line/terminal, the generic usage
is:
```shell
main.py [-h] [--dont-load-history] [--dont-save-history]
               [--delay DELAY] [--history-filename HISTORY_FILENAME]
               [--to-mp3] [--ffmpeg-exe FFMPEG_EXE] [--adjust-mp3-gain]
               [--target-mp3-gain TARGET_MP3_GAIN] [--mp3gain-exe MP3GAIN_EXE]
               url output-path
```

Simple usage from the command line:
```shell
python main.py https://www.youtube.com/playlist?list=ACF5.... C:/TEMP
```

There are command line arguments available (note `url` and `output-path` are mandatory positional arguments):


| Parameter | Meaning | Value |
| --------- | ------- | ---------- |
| url       | The URL of the input YouTube playlist, e.g. `https://www.youtube.com/playlist?list=OLAK5...` | Mandatory. |
| output&#8209;path | The output path (absolute or relative) where the result will be stored. | Mandatory. |
| &#8209;&#8209;dont&#8209;load&#8209;history | If set, the previously downloaded tracks will be downloaded again. | Optional. If not set, history is loaded by default. |
| &#8209;&#8209;dont&#8209;save&#8209;history | If set, the list of downloaded tracks will not be saved for future history use. | Optional. If not set, history is saved by default. |
| &#8209;&#8209;history&#8209;filename | Sets the custom history filename, if required. May be absolute or relative. If relative, the file is stored in the output path. | Optional. If not set, default name is used. |
| &#8209;&#8209;delay | Sets the gap (sleep interval) in seconds between download end/start (to not overhaul YouTube server). | Optional. Default value is 10. |
| &#8209;&#8209;to&#8209;mp3 | If set, the program will convert downloaded `*.webm` files into `*.mp3` files using FFMPEG. If the conversion is successful, the `*.webm` files are deleted. | Optional. Conversion is not done by default. |
| &#8209;&#8209;ffmpeg&#8209;exe | Location (absolute or relative) to `ffmpeg.exe` file, including the filename. If not set, the `PATH` environment variable is used to detect the file location. If the file is not found, the script will crash. | Optional. Uses `PATH` environment variable by default.
| &#8209;&#8209;adjust-mp3-gain | If set, the program will try to adjust volume of MP3 file using `mp3_gain.exe`. | Optional. Adjust is not done by default.
| &#8209;&#8209;target-mp3-gain | Use custom target mp3 gain. Integer value expected. | If not set, default value 89 is used.
| &#8209;&#8209;mp3gain-exe | Location (absolute or relative) to `mp3_gain.exe` file, including the filename. If not set, the `PATH` environment variable is used to detect the file location. if the file is not found, the script will crash. | Optional. Uses `PATH` environment variable by default.

More complex usage:

```shell
python main.py 
  --dont-load-hstory 
  --delay 10 
  --to-mp3 
  --ffmpeg-exe "c:/program files/ffmpeg/ffmpeg.exe"
  --adjust-mp3-gain
  --target-mp3-gain 93
  --mp3gain-exe "C:/program files/mp3gain/mp3gain.exe" 
  https://www.youtube.com/playlist?list=ACF5... 
  C:/TEMP
```

   


