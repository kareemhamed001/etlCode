import pandas

from app.etl.DataSoruces.DataSource import DataSource 
from app.ModelGenerator.main import *
class ModelDs(DataSource):
    
    def __init__(self, _data: pandas.DataFrame = None, _isThread=False) -> None:
        super().__init__(_data, _isThread)
        DataSource.results = None

    def extract(self, _sorucePath:str) -> str:
        self._sorucePath=_sorucePath

    def load(self, _destinationPath:str,_modelType:str) -> str:
        ModelGenerator(self._sorucePath,_destinationPath,_modelType)
       