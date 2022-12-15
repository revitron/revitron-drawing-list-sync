import csv
import datetime
from drawinglistsync.collections import Revision, Revisions, RevisionsList

REVISIONS_MAX_COLS = 750


def getDateFromString(dateString):
	return datetime.datetime.strptime(dateString, r'%d.%m.%Y')


def getRevisionCols(rows, revisionsRow):
	row = rows[revisionsRow - 1]
	return [(value, row[value]) for value in row if row[value]]


def getRevisionsFromCsv(file, revisionsRow, sheetNumberCol, format):
	revisionsList = RevisionsList()
	rows = []
	with open(file) as f:
		reader = csv.DictReader(f, range(1, REVISIONS_MAX_COLS))
		for row in reader:
			rows.append(row)
	revisionCols = getRevisionCols(rows, revisionsRow)
	for n in range(revisionsRow, len(rows)):
		row = rows[n]
		nr = row[sheetNumberCol]
		if not nr:
			continue
		sheetRevisions = Revisions()
		for item in revisionCols:
			col = item[0]
			if not row[col]:
				continue
			rev = Revision(row[col], item[1], format)
			date = getDateFromString(rev.date)
			sheetRevisions.add(rev)
			if date >= datetime.datetime.now():
				break
		revisionsList.add(nr, sheetRevisions)
	return revisionsList


class RevisionFormat(object):

	maxCharsIndex = None
	maxCharsDate = None
	maxCharsTitle = None

	def __init__(self, config):
		self.maxCharsIndex = config.maxCharsIndex
		self.maxCharsDate = config.maxCharsDate
		self.maxCharsTitle = config.maxCharsTitle