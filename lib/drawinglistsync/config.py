from revitron import DocumentConfigStorage

CONFIG_KEY = 'revitron.drawing-list-sync'


class Config:

	xlsFile = ''
	parameterRow = ''
	revisionsRow = ''
	worksheet = ''

	def __init__(self):
		config = DocumentConfigStorage().get(CONFIG_KEY, dict())
		self.xlsFile = config.get('xlsFile', '')
		self.parameterRow = int(config.get('parameterRow', '1'))
		self.revisionsRow = int(config.get('revisionsRow', '2'))
		self.worksheet = config.get('worksheet', 'Sheets')
