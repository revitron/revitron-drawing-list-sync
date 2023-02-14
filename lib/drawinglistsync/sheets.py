from revitron import _, DB, DOC
import drawinglistsync.date
import drawinglistsync.config
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
					# conversion of US formated dates from CSV to configured format
					if drawinglistsync.date.isUsDate(value):
							value = drawinglistsync.date.normalizeDateString(value,
													 config.dateFormat)
					_(sheet).set(key, value)
			sheetRevisions = revisionList.get(number)
			if sheetRevisions:
				_(sheet).set(config.revisionsField, str(sheetRevisions), 'MultilineText')


def createSheet():
	invalid = DB.ElementId.InvalidElementId
	return DB.ViewSheet.Create(DOC, invalid)