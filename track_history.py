import json

DEFAULT_HISTORY_FILE_NAME = "__downloaded.yt.json"


class TrackHistory:

    def __init__(self):
        self.title = None
        self.stream_id = None
        self.date = None
        self.target_file = None
        self.abr = None
        self.status = None


def try_load_track_history(history_file_name):
    ret = {}
    with open(history_file_name, "r") as f:
        tmp = json.load(f)
    for key in tmp.keys():
        val = tmp[key]
        trk = TrackHistory()
        trk.title = val["title"]
        trk.date = val["date"]
        trk.target_file = val["file"]
        trk.stream_id = val["stream_id"]
        trk.abr = val["abr"] if "abr" in val.keys() else None
        trk.status = val["status"]
        ret[key] = trk
    return ret


def save_track_history(tracks, history_file_name):
    dct = {}
    for key in tracks.keys():
        trk = tracks[key]
        tmp = {"title": trk.title,
               "date": trk.date,
               "file": trk.target_file,
               "stream_id": trk.stream_id,
               "status": trk.status}
        if trk.abr is not None:
            trk.abr = str(trk.abr)
        dct[key] = tmp
    with open(history_file_name, "w") as f:
        json.dump(dct, f, indent=2)
