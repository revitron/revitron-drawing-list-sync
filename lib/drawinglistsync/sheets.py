from revitron import _, DB, DOC
from pyrevit import forms


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
	invalid = DB.ElementId.InvalidElementId
	return DB.ViewSheet.Create(DOC, invalid)