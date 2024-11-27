# This is a simple testing script validating if YouTube download is working

from pytubefix import Playlist, YouTube
import logging
import time

playlist_url = "https://www.youtube.com/watch?v=FxMtO7HvXzA&list=PLF273091A22D1723E"
out_path = "R:/"

logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum level of logs to display
    format='%(asctime)s - %(levelname)s - %(message)s'  # Customize log message format
)

ypl = Playlist(playlist_url)
track_count = len(ypl.video_urls)
try:
    logging.info(f"Found playlist '{ypl.title}' with {track_count} tracks")
except Exception as ex:
    logging.error(f"ERROR: Failed to download the playlist. Check it is NOT PRIVATE.")
    raise (ex)
logging.info("Looking for videos...")
for index, url in enumerate(ypl.video_urls):
    if index > 1:
        break  # only two tracks are downloaded for testing purposes
    logging.info(f"{index + 1}. of {track_count}")


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


    try:
        yt = YouTube(url)
        ys, abr = _get_best_audio_stream(yt)
        final_file_name = ys.download(output_path=out_path)
        logging.info(f"Downloaded as {final_file_name}")
    except Exception as e:
        logging.error("\tVideo " + str(index) + " :: " + url + " erroneous, will be not downloaded: " + e.__str__())

    time.sleep(1)

logging.info("Done")
