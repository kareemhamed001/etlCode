import pandas
import regex as re
from queue import Queue


# Aggregation Functions that is used in SQL
class compilerAggregationFunction:
    def __init__(self, _data: pandas.DataFrame, _filters: dict) -> None:
        self.Data = _data
        self.left = _filters['left']
        self.right = _filters['right']

        self.AggFunctions = {
            'or': lambda: self.Or(),
            'and': lambda: self.And(),
            'like': lambda: self.Like(),
            '>': lambda: self.GreaterThan(),
            '>=': lambda: self.GreaterOrEqual(),
            '<': lambda: self.LessThan(),
            '<=': lambda: self.LessOrEqual(),
            '==': lambda: self.Equal(),
            '!=': lambda: self.NotEqual(),
        }

    def Or(self):
        self.Data = pandas.concat([self.left, self.right])
        return self.Data[~ self.Data.index.duplicated(keep='first')]

    def And(self):
        self.Data = pandas.merge([self.left, self.right])
        return self.Data[~ self.Data.index.duplicated(keep='first')]

    def Like(self):
        return self.Data[[True if re.match(self.right, str(x)) else False for x in self.Data[self.left]]]

    def GreaterThan(self):
        return self.Data[self.Data[self.left] > self.right]

    def GreaterOrEqual(self):
        return self.Data[self.Data[self.left] >= self.right]

    def LessThan(self):
        return self.Data[self.Data[self.left] < self.right]

    def LessOrEqual(self):
        return self.Data[self.Data[self.left] <= self.right]

    def Equal(self):
        return self.Data[self.Data[self.left] == self.right]

    def NotEqual(self):
        return self.Data[self.Data[self.left] != self.right]


# File extensions Parent Class
class DataSource:
    results = None

    def __init__(self, _data: Queue = None, _isThread=False) -> None:
        # _data is None because it may extract data from external file
        # Operation is assigned in transform function
        self.Operation = dict()
        self.Data: Queue = _data
        self.isThread = False
        self.TargetMethod = None

    def extract(self, _sorucePath: str) -> pandas.DataFrame:
        raise NotImplementedError

    def load(self, _destinationPath: str) -> None:
        raise NotImplementedError

    # For threads
    def run(self):
        raise NotImplementedError

    # return data that is transformed
    def transform(self, _operation: dict) -> Queue:
        # default data if nothing change
        self.TargetMethod = "transform"
        q = Queue()
        transformedData = self.QueueData()
        self.Operation = _operation
        if self.Operation['FILTER']:
            transformedData = self.getFilter(transformedData)
        if self.Operation['COLUMNS'] != '__all__':
            transformedData = self.getColumns(transformedData)
        if self.Operation['DISTINCT']:
            transformedData = self.getDistinct(transformedData)
        if self.Operation['ORDER']:
            transformedData = self.getOrder(transformedData)
        if self.Operation['LIMIT']:
            transformedData = self.getLimit(transformedData)
        q.put(transformedData)
        return q

    # return Filtered Data
    def getFilter(self, data) -> pandas.DataFrame:
        Agg = compilerAggregationFunction(data, self.Operation['FILTER'])
        filter = self.Operation['FILTER']['type']
        temp = Agg.AggFunctions[filter]()
        return temp

    # return specific columns
    def getColumns(self, data) -> pandas.DataFrame:
        return data.filter(items=self.Operation['COLUMNS'])

    # remove duplications from data
    def getDistinct(self, data) -> pandas.DataFrame:
        return data.drop_duplicates()

    # sort data
    def getOrder(self, data) -> pandas.DataFrame:
        columnn = self.Operation['ORDER'][0]
        return data.sort_values(columnn, ascending=self.Operation['ORDER'][1] == 'ASC')

    # return data in a certain range
    def getLimit(self, data) -> pandas.DataFrame:
        return data[:self.Operation['LIMIT']]

    def QueueData(self):
        return self.Data.get()
