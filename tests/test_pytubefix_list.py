from pytubefix import Playlist, YouTube

LIST_URL = "https://www.youtube.com/playlist?list=PLF273091A22D1723E" ## etrance
# LIST_URL = "https://www.youtube.com/playlist?list=PL0bQQrRRNSOJ37BRHvXuG5e2HG1GlHime" ## ehouse
ypl = Playlist(LIST_URL)
track_count = len(ypl.video_urls)
print(f"Found playlist '{ypl.title}' with {track_count} tracks")