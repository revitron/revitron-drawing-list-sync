import revitron
import csv
from revitron import _
from os import system
from os.path import dirname, join
from tempfile import mkdtemp
from System.Collections.Generic import Dictionary

CONFIG_KEY = 'revitron.drawing-list-sync'
PARAM_MAX_COLS = 25


def createCsvFiles(xls):
	tmp = mkdtemp()
	convert = join(dirname(__file__), 'convert.bat')
	csvSheets = join(tmp, 'sheets.csv')
	csvGroups = join(tmp, 'groups.csv')
	system('{} {} {} {}'.format(convert, xls, csvSheets, csvGroups))
	return csvSheets, csvGroups


def getGroupsFromCsv(file):
	groups = []
	with open(file) as f:
		reader = csv.DictReader(f, ['a', 'b', 'category'])
		for row in reader:
			groups.append(row['category'])
	return groups


def getParameterCols(rows, parameterRow):
	row = rows[parameterRow - 1]
	return [(value, row[value]) for value in row if row[value]]


def getSheetsFromCsv(file, parameterRow):
	drawingList = DrawingList()
	rows = []
	with open(file) as f:
		reader = csv.DictReader(f, range(1, PARAM_MAX_COLS))
		for row in reader:
			rows.append(row)
	parameterCols = getParameterCols(rows, parameterRow)
	sheetNumberCol = [item[0] for item in parameterCols if item[1] == 'Sheet Number'][0]
	for n in range(parameterRow, len(rows)):
		row = rows[n]
		nr = row[sheetNumberCol]
		if nr:
			data = {}
			for item in parameterCols:
				col = item[0]
				name = item[1]
				data[name] = row[col]
			drawingList.add(nr, data)
	return drawingList


def createOrUpdateSheets(drawingList, collection):
	for item in drawingList.all():
		number = item.Key
		data = item.Value
		sheet = collection.get(number)
		if not sheet:
			sheet = createSheet()
		for key, value in data.items():
			_(sheet).set(key, value)


def createSheet():
	invalid = revitron.DB.ElementId.InvalidElementId
	return revitron.DB.ViewSheet.Create(revitron.DOC, invalid)


class Config:

	xlsFile = ''
	parameterRow = ''

	def __init__(self):
		config = revitron.DocumentConfigStorage().get(CONFIG_KEY, dict())
		self.xlsFile = config.get('xlsFile', '')
		self.parameterRow = int(config.get('parameterRow', '1'))


class GenericCollection:

	valueType = dict

	def __init__(self):
		self._collection = Dictionary[str, self.valueType]()

	def add(self, key, data):
		self._collection.Add(str(key), data)

	def get(self, key):
		success, value = self._collection.TryGetValue(str(key))
		return value

	def all(self):
		return self._collection.GetEnumerator()


class DrawingList(GenericCollection):
	valueType = dict


class ModelSheetCollection(GenericCollection):
	valueType = revitron.DB.ViewSheet
