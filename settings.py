from pathlib import Path


class PathsData(object):

    def __init__(self):

        self.yt_folder = Path.cwd().joinpath('yt_download')
        self.processed_folder = Path.cwd().joinpath('processed_audio')
        if not self.yt_folder.is_dir():
            self.yt_folder.mkdir(parents=True, exist_ok=True)
        if not self.processed_folder.is_dir():
            self.processed_folder.mkdir(parents=True, exist_ok=True)


paths_data = PathsData()
