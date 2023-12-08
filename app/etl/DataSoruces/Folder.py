from app.FrameProcessor.Loader.loader import Loader
from app.FrameProcessor.Extract.extract import Extract
from queue import Queue
import pandas

class FolderDS:

    def __init__(self, data = None, _isThread = False) -> None:
        self.Data = data
        self.Dict = []

    def extract(self, _source):
        pass

    def transform(self, _operation):
       pass