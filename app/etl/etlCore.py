from app.etl.DataSoruces.FlatFile import *
from app.etl.DataSoruces.Database import *
from app.etl.DataSoruces.BinaryFile import BirdDetector
from app.etl.DataSoruces.Folder import FolderDS
from app.etl.DataSoruces.Model import *
from app.ModelGenerator.main import *
class etl:
    ClassType = {
            "csv": lambda x, y: CsvDS(x,y),
            "sqlite": lambda x, y: SqliteDS(x,y),
            "mssql": lambda x, y: MssqlDS(x,y),
            "html": lambda x, y: HtmlDS(x,y),
            "json": lambda x, y: JsonDF(x,y),
            "xml": lambda x, y: XmlDS(x,y),
            "excel": lambda x, y: ExcelDS(x,y),
            # "video": lambda x,y : BirdDetector(x,y),
            "folder": lambda x,y: FolderDS(x,y),
            "model":lambda x,y: ModelDs(x,y),
            "console" : lambda x, y: ConsolDS(x,y)
    }
    def __init__(self, _sorucePath:str, _destinationPath:str, __opData:list) -> None:
        self.isThread = False
        self.SourceType=''
        self.DestinationPath=''
        self.SourceType = _sorucePath.split('::')[0].lower()
        self.SourcePath = _sorucePath.split('::')[1].lower()
        self.DestinationType = _destinationPath.split('::')[0].lower()
        self.DestinationPath = _destinationPath.split('::')[1].lower() if _destinationPath.split('::')[0].lower() != "console" else None
        self.OpData = __opData
        self.Data = pandas.DataFrame()
        
    # Get DataSoruce Object base one Source file type
    def __Pathtype(self,type, _data = None) -> DataSource:
        return self.ClassType[type](_data, self.isThread)

    def ExtractData(self):
        self.ExtrClass = self.__Pathtype(self.SourceType)
        self.ExtrData = self.ExtrClass.extract(self.SourcePath)

    def TransformData(self):
        self.TransClass = self.__Pathtype(self.SourceType,self.ExtrData)
        self.TransData = self.TransClass.transform(self.Operation)

    def LoadData(self):
        self.LoadClass = self.__Pathtype(self.DestinationType,self.TransData)
        self.LoadClass.load(self.DestinationPath)

    def SetupThread(self):
        self.isThread = True
    
    #thread is implemented only in for video (Detector)
    def StartThread(self):

        if self.OpData['operation_type']=='train':
            ModelGenerator(self.SourcePath,self.DestinationPath,str(self.OpData['model']),self.OpData['epoch'],self.OpData['batchsize'])
        else:
            self.ExtrClass.start()
            self.TransClass.start()
            self.LoadClass.start() 

