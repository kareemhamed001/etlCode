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
    def __init__(self, _sorucePath:str, _destinationPath:str, _ColumnList:list) -> None:
        self.isThread = False
        self._getPathesAndTypes(_sorucePath,_destinationPath,_ColumnList['operation_type'])
        self.ColumnList = _ColumnList
        self.Data = pandas.DataFrame()

    def _getPathesAndTypes(self,sourcePath,destinationPath,operationType):
        if operationType=='train':
            self.SourceType = ''
            self.SourcePath = ''
            self.DestinationType =''
            self.DestinationPath=''
        else:
            self.SourceType = sourcePath.split('::')[0].lower()
            self.SourcePath = sourcePath.split('::')[1].lower()
            self.DestinationType = destinationPath.split('::')[0].lower()
            self.DestinationPath = destinationPath.split('::')[1].lower() if destinationPath.split('::')[0].lower() != "console" else None
            
    # Get DataSoruce Object base one Source file type
    def __SoruceType(self, _data = None) -> DataSource:
        return self.ClassType[self.SourceType](_data, self.isThread)

    # Get DataSoruce Object base one Destination file type
    def __DestinationType(self, _data = None) -> DataSource:
        return self.ClassType[self.DestinationType](_data, self.isThread)

    def ExtractData(self):
        self.ExtrClass = self.__SoruceType()
        self.ExtrData = self.ExtrClass.extract(self.SourcePath)

    def TransformData(self):
        self.TransClass = self.__SoruceType(self.ExtrData)
        self.TransData = self.TransClass.transform(self.Operation)

    def LoadData(self):
        self.LoadClass = self.__DestinationType(self.TransData)
        self.LoadClass.load(self.DestinationPath)

    def SetupThread(self):
        self.isThread = True
    
    #thread is implemented only in for video (Detector)
    def StartThread(self):
        if self.SourceType == "video":
            self.ExtrClass.start()
            self.TransClass.start()
            self.LoadClass.start()
        if self.ColumnList['operation_type']=='train':
                ModelGenerator(str(self.ColumnList['source']),str(self.ColumnList['destination']),str(self.ColumnList['model']))
            

