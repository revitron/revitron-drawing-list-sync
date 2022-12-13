import csv
from revitron import _
from drawinglistsync.collections import *
from drawinglistsync.config import *
from drawinglistsync.sheets import *
from os import system
from os.path import dirname, join
from tempfile import mkdtemp

PARAM_MAX_COLS = 25


def createCsvFile(xls, worksheet):
	tmp = mkdtemp()
	convert = join(dirname(__file__), 'convert.bat')
	csvSheets = join(tmp, 'sheets.csv')
	system('{} {} {} {}'.format(convert, xls, worksheet, csvSheets))
	return csvSheets


def getParameterCols(rows, parameterRow):
	row = rows[parameterRow - 1]
	return [(value, row[value]) for value in row if row[value]]


def getDrawinglistFromCsv(file, parameterRow):
	drawingList = DrawingList()
	rows = []
	with open(file) as f:
		reader = csv.DictReader(f, range(1, PARAM_MAX_COLS))
		for row in reader:
			rows.append(row)
	parameterCols = getParameterCols(rows, parameterRow)
	sheetNumberCol = [item[0] for item in parameterCols if item[1] == 'Sheet Number'][0]
	for n in range(parameterRow, len(rows)):
		row = rows[n]
		nr = row[sheetNumberCol]
		if nr:
			data = {}
			for item in parameterCols:
				col = item[0]
				name = item[1]
				data[name] = row[col]
			drawingList.add(nr, data)
	return drawingList
