import re
import datetime
from revitron import DB
from System.Collections.Generic import Dictionary


def normalizeDateString(dateString):
	date = datetime.datetime.strptime(dateString, r'%d.%m.%Y')
	return date.strftime(r'%d.%m.%Y')


class GenericCollection(object):

	valueType = dict

	def __init__(self):
		self._collection = Dictionary[str, self.valueType]()

	def add(self, key, data):
		self._collection.Add(str(key), data)

	def get(self, key):
		success, value = self._collection.TryGetValue(str(key))
		return value

	def all(self):
		return self._collection.GetEnumerator()


class DrawingList(GenericCollection):
	valueType = dict


class ModelSheetCollection(GenericCollection):
	valueType = DB.ViewSheet


class Revision(object):

	index = ''
	date = ''
	title = ''

	def __init__(self, index, text):
		matches = re.match('^(\d{1,2}\.\d{1,2}\.\d{4})(.*)$', text, re.MULTILINE)
		self.index = index.ljust(5)
		try:
			self.date = normalizeDateString(matches.group(1)).ljust(14)
			self.title = matches.group(2).lstrip()
		except:
			pass

	def __str__(self):
		return '{}{}{}'.format(self.index, self.date, self.title)


class Revisions(GenericCollection):

	valueType = Revision

	def __str__(self):
		text = ''
		for rev in self._collection:
			text += str(rev.Value) + '\r\n'
		return text

	def add(self, revision):
		key = '{}_{}'.format(revision.index, revision.date)
		_rev = self.get(key)
		if _rev:
			_rev.title += ' / {}'.format(revision.title)
		else:
			self._collection.Add(key, revision)


class RevisionsList(GenericCollection):

	valueType = Revisions
