from pathlib import Path

from app.FrameProcessor.Loader.loader import Loader
from app.FrameProcessor.Extract.extract import Extract
from queue import Queue
import pandas
import os


class FolderDS:

    def __init__(self, dataQueue: Queue = None, _isThread=False) -> None:
        self.Data: Queue = dataQueue

    def extract(self, _source):

        if os.path.exists(_source) and os.path.isdir(_source):

            all_data = os.listdir(_source)

            files_only = [item for item in all_data if os.path.isfile(os.path.join(_source, item))]

            subdirectories_only = [os.path.join(_source, item) for item in all_data if
                                   os.path.isdir(os.path.join(_source, item))]

            return files_only, subdirectories_only
        else:
            print(f"The folder path {_source} does not exist or is not a directory.")
            raise FileExistsError(f"The folder path {_source} does not exist or is not a directory.")

    def transform(self, _operation):
        pass

    def load(self, _destination):
        if not Path(_destination).exists():
            Path(_destination).mkdir(parents=True, exist_ok=True)
