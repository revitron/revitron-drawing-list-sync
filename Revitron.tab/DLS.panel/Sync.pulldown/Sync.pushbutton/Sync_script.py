from revitron import Filter, Transaction, _
from drawinglistsync import Config, createCsvFile, getSheetsFromCsv, createOrUpdateSheets, ModelSheetCollection
from pyrevit import forms

config = Config()

if not config.xlsFile or not config.parameterRow:
	forms.alert('Please first configure the synching!', exitscript=True)

collection = ModelSheetCollection()

for item in Filter().byCategory('Sheets').noTypes().getElements():
	collection.add(_(item).get('Sheet Number'), item)

csvSheets = createCsvFile(config.xlsFile, config.worksheet)
sheetData = getSheetsFromCsv(csvSheets, config.parameterRow)

with Transaction():
	createOrUpdateSheets(sheetData, collection)
