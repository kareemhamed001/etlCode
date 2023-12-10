from app.etl.DataSoruces.FlatFile import *
from app.etl.DataSoruces.Database import *
from app.etl.DataSoruces.BinaryFile import BirdDetector
from app.etl.DataSoruces.Folder import FolderDS
from app.etl.DataSoruces.Model import *
from app.ModelGenerator.main import *
from queue import Queue


class etl:
    ClassType = {
        "csv": lambda x, y: CsvDS(x, y),
        "sqlite": lambda x, y: SqliteDS(x, y),
        "mssql": lambda x, y: MssqlDS(x, y),
        "html": lambda x, y: HtmlDS(x, y),
        "json": lambda x, y: JsonDF(x, y),
        "xml": lambda x, y: XmlDS(x, y),
        "excel": lambda x, y: ExcelDS(x, y),
        "video": lambda x, y: BirdDetector(x, y),
        "folder": lambda x, y: FolderDS(x, y),
        "model": lambda x, y: ModelDs(x, y),
        "console": lambda x, y: ConsolDS(x, y)
    }

    def __init__(self, _sourcePath: str, _destinationPath: str, __opData: dict) -> None:
        self.LoadClass = None
        self.TransData = None
        self.TransClass = None
        self.ExtrData = None
        self.ExtrClass = None
        self.isThread = False
        self.SourceType = ''
        self.DestinationPath = ''
        self.SourceType = _sourcePath.split('::')[0].lower()
        self.SourcePath = _sourcePath.split('::')[1]
        self.DestinationType = _destinationPath.split('::')[0].lower()
        self.DestinationPath = _destinationPath.split('::')[1] if _destinationPath.split('::')[
                                                                      0].lower() != "console" else None
        self.OpData = __opData
        self.dataQueue = Queue()

    def __Pathtype(self, type, _data=None) -> DataSource:
        return self.ClassType[type](_data, self.isThread)

    def __ExtractData(self):
        ExtrClass = self.__Pathtype(self.SourceType, self.dataQueue)
        self.ExtrData = ExtrClass.extract(self.SourcePath)
        return self.ExtrData

    def __TransformData(self, _data):
        self.TransClass = self.__Pathtype(self.SourceType, _data)
        self.TransData = self.TransClass.transform(self.OpData)
        return self.TransData

    def __LoadData(self, _data):
        self.LoadClass = self.__Pathtype(self.DestinationType, _data)
        self.LoadClass.load(self.DestinationPath)

    def SetupThread(self):
        self.isThread = True

    # thread is implemented only in for video (Detector)
    def Start(self):
        if self.OpData['operation_type'] == 'select':
            dataExtracted = self.__ExtractData()
            dataTransformed = self.__TransformData(dataExtracted)
            self.__LoadData(dataTransformed)

        elif self.OpData['operation_type'] == 'train':
            if self.SourceType == 'folder':
                dataExtracted = self.__ExtractData()

                ModelGenerator(self.SourcePath, dataExtracted[1], self.OpData['model'], self.OpData['epoch'],
                               self.OpData['batchsize'])
