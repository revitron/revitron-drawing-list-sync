from revitron import _, DB, DOC
import date
import re

def createOrUpdateSheets(drawingList, revisionList, modelSheetCollection, config):
	for item in drawingList.all():
		number = item.Key
		data = item.Value
		sheet = modelSheetCollection.get(number)
		if not sheet and config.createMissingSheets:
			sheet = createSheet()
		if not sheet:
			continue
		if _(sheet).isNotOwned():
			for key, value in data.items():
				if _(sheet).getParameter(key).exists() or config.createMissingParameters:
					# conversion of US formated dates from CSV to defined format
					if date.isUSDate(value):
							value = date.normalizeDateString(value, date.DATE_FORMATS[0])
					_(sheet).set(key, value)
			sheetRevisions = revisionList.get(number)
			if sheetRevisions:
				_(sheet).set(config.revisionsField, str(sheetRevisions), 'MultilineText')


def createSheet():
	invalid = DB.ElementId.InvalidElementId
	return DB.ViewSheet.Create(DOC, invalid)