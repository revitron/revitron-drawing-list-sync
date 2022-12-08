import revitron
from drawinglistsync import Config, CONFIG_KEY
from revitron.ui import SimpleWindow, TextBox

config = Config()

window = SimpleWindow('Drawing List Sync Configuration', width=550, height=250)

TextBox.create(window, 'Main', 'xlsFile', config.xlsFile, title='Excel File Path')
TextBox.create(
    window,
    'Main',
    'parameterRow',
    config.parameterRow,
    title='Parameter Name Row Number'
)

window.show()

if window.ok:
	revitron.DocumentConfigStorage().set(CONFIG_KEY, window.values)
