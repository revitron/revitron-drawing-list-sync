from revitron import Filter, Transaction, _
from drawinglistsync import (
    Config,
    createCsvFile,
    getDrawinglistFromCsv,
    getRevisionsFromCsv,
    createOrUpdateSheets,
    ModelSheetCollection,
    RevisionsList
)
from pyrevit import forms

config = Config()

if not config.xlsFile or not config.parameterRow or not config.revisionsRow:
	forms.alert('Please first configure the synching!', exitscript=True)

modelSheetCollection = ModelSheetCollection()

for item in Filter().byCategory('Sheets').noTypes().getElements():
	modelSheetCollection.add(_(item).get('Sheet Number'), item)

csvSheets = createCsvFile(config.xlsFile, config.worksheet)
drawingList, sheetNumberCol = getDrawinglistFromCsv(csvSheets, config.parameterRow)
revisionList = RevisionsList()

if (config.revisionsEnabled):
	revisionList = getRevisionsFromCsv(csvSheets, config.revisionsRow, sheetNumberCol)

with Transaction():
	createOrUpdateSheets(
	    drawingList, revisionList, modelSheetCollection, config.revisionsField
	)
