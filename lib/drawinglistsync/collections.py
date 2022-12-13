from revitron import DB
from System.Collections.Generic import Dictionary


class GenericCollection:

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