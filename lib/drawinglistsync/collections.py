import re
import datetime
from revitron import DB
from System.Collections.Generic import Dictionary

DATE_REGEX = '(\d{1,2}\.\d{1,2}\.\d{4}|\d{6}|\d{4}-\d{2}-\d{2})'


def normalizeDateString(dateString, outputFormat):
	formats = [
	    r'%d.%m.%Y',  # 31.01.2023
	    r'%y%m%d',  # 230131
	    r'%Y-%m-%d',  # 2023-01-31
	]
	for format in formats:
		try:
			date = datetime.datetime.strptime(dateString, format)
			if date:
				return date.strftime(outputFormat)
		except:
			pass
	return ''


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
	format = None

	def __init__(self, index, text, format):
		matches = re.match('^' + DATE_REGEX + '(.*)$', text, re.MULTILINE)
		self.index = index.ljust(format.maxCharsIndex)
		self.format = format
		try:
			date = normalizeDateString(matches.group(1), format.dateFormat)
			self.date = date.ljust(format.maxCharsDate)
			title = matches.group(2).lstrip()
			if len(title) > format.maxCharsTitle:
				title = title[:format.maxCharsTitle] + ' ...'
			self.title = title
		except:
			pass

	def __str__(self):
		return '{} {} {}'.format(self.index, self.date, self.title)


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
			space = (_rev.format.maxCharsIndex + _rev.format.maxCharsDate + 2) * ' '
			_rev.title += '\r\n{}{}'.format(space, revision.title)
		else:
			self._collection.Add(key, revision)


class RevisionsList(GenericCollection):

	valueType = Revisions
