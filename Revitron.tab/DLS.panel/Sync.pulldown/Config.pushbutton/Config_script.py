import revitron
from drawinglistsync import Config, CONFIG_KEY
from revitron.ui import TabWindow, TextBox, CheckBox

config = Config()
window = TabWindow(
    'Drawing List Sync Configuration', ['Sheets', 'Revisions'], width=550, height=360
)

TextBox.create(window, 'Sheets', 'xlsFile', config.xlsFile, title='Excel File Path')

TextBox.create(
    window, 'Sheets', 'worksheet', str(config.worksheet), title='Worksheet Drawing List'
)

TextBox.create(
    window,
    'Sheets',
    'parameterRow',
    str(config.parameterRow),
    title='Parameter Name Row Number'
)

CheckBox.create(
    window,
    'Revisions',
    'revisionsEnabled',
    config.revisionsEnabled,
    title='Enable Parsing Revisions'
)

TextBox.create(
    window,
    'Revisions',
    'revisionsRow',
    str(config.revisionsRow),
    title='Revisions Row Number'
)

TextBox.create(
    window,
    'Revisions',
    'revisionsField',
    str(config.revisionsField),
    title='Revisions Text Parameter Name'
)

window.show()

if window.ok:
	revitron.DocumentConfigStorage().set(CONFIG_KEY, window.values)
