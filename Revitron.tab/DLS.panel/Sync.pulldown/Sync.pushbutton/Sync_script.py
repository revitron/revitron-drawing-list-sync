from revitron import Filter, Selection, Transaction, _
from drawinglistsync import (
    Config,
    createCsvFiles,
    getGroupsFromCsv,
    getSheetsFromCsv,
    createOrUpdateSheets,
    ModelSheetCollection
)
from pyrevit import forms

config = Config()

if not config.xlsFile or not config.parameterRow:
	forms.alert('Please first configure the synching!', exitscript=True)

selected = None
selection = Selection.get()

if selection:
	selected = Filter(Selection.get()).byCategory('Sheets').noTypes().getElements()

if not selected:
	optionAll = 'Synchronize all sheets'
	optionCancel = 'Cancel'
	res = forms.alert(
	    'No sheets selected. Synchronize all sheets instead?',
	    options=[optionAll, optionCancel]
	)

	if res == optionAll:
		selected = Filter().byCategory('Sheets').noTypes().getElements()

collection = ModelSheetCollection()

for item in selected:
	collection.add(_(item).get('Sheet Number'), item)

csvSheets, csvGroups = createCsvFiles(config.xlsFile)
groups = getGroupsFromCsv(csvGroups)
sheetData = getSheetsFromCsv(csvSheets, config.parameterRow)

with Transaction():
	createOrUpdateSheets(sheetData, collection)
