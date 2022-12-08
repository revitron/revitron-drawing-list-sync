import revitron
from drawinglistsync import Config, CONFIG_KEY
from revitron.ui import SimpleWindow, TextBox

config = Config()
window = SimpleWindow('Drawing List Sync Configuration', width=550, height=375)

TextBox.create(window, 'Main', 'xlsFile', config.xlsFile, title='Excel File Path')

TextBox.create(
    window, 'Main', 'worksheet', str(config.worksheet), title='Worksheet Drawing List'
)

TextBox.create(
    window,
    'Main',
    'parameterRow',
    str(config.parameterRow),
    title='Parameter Name Row Number'
)

TextBox.create(
    window,
    'Main',
    'revisionsRow',
    str(config.revisionsRow),
    title='Revisions Row Number'
)

window.show()

if window.ok:
	revitron.DocumentConfigStorage().set(CONFIG_KEY, window.values)
