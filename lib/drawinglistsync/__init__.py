import revitron
import csv
from revitron import _
from os import system
from os.path import dirname, join
from tempfile import mkdtemp
from System.Collections.Generic import Dictionary
from pyrevit import forms

CONFIG_KEY = 'revitron.drawing-list-sync'
PARAM_MAX_COLS = 25


def createCsvFile(xls, worksheet):
	tmp = mkdtemp()
	convert = join(dirname(__file__), 'convert.bat')
	csvSheets = join(tmp, 'sheets.csv')
	system('{} {} {} {}'.format(convert, xls, worksheet, csvSheets))
	return csvSheets


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


def confirmParameterCreation(key):
	optionCreate = 'Create parameter "{}"'.format(key)
	optionCancel = 'Skip parameter'
	res = forms.alert(
	    'The parameter "{}" does not exist in the current model. Do you want to create it?'
	    .format(key),
	    options=[optionCreate, optionCancel]
	)
	if res == optionCreate:
		return True
	return False


def createOrUpdateSheets(drawingList, collection):
	skipped = []
	for item in drawingList.all():
		number = item.Key
		data = item.Value
		sheet = collection.get(number)
		if not sheet:
			sheet = createSheet()
		if _(sheet).isNotOwned():
			for key, value in data.items():
				if not _(sheet).getParameter(key).exists():
					if key in skipped:
						continue
					if not confirmParameterCreation(key):
						skipped.append(key)
						continue
				_(sheet).set(key, value)


def createSheet():
	invalid = revitron.DB.ElementId.InvalidElementId
	return revitron.DB.ViewSheet.Create(revitron.DOC, invalid)


class Config:

	xlsFile = ''
	parameterRow = ''
	revisionsRow = ''
	worksheet = ''

	def __init__(self):
		config = revitron.DocumentConfigStorage().get(CONFIG_KEY, dict())
		self.xlsFile = config.get('xlsFile', '')
		self.parameterRow = int(config.get('parameterRow', '1'))
		self.revisionsRow = int(config.get('revisionsRow', '2'))
		self.worksheet = config.get('worksheet', 'Sheets')


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
