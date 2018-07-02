""",------------------------------,
  /	 Spreadsheet De-Duplicator   /
 /	Author: Jacob Clark			/
/______________________________/
	
	This program removes duplicate entries from a CSV file.
	This program assumes that the columns are delimited ONLY by commas.
"""

import csv
from collections import defaultdict

"""
Only consider entries that share the same business name!
From there, we only want the entry with the most complete information.
If multiple have complete information, delete one.

Guy Properties, (865) 430-5640, 1239 Appalachian Ln, Gatlinburg, TN, 37738
Guy Properties, (865) 325-1010, 245 Eagle Rd, Gatlinburg, TN, 37738, http://www.smokymtndreams.com/
Guy Properties, (865) 436-8460, 644 Timber Ridge Rd, Gatlinburg, TN, 37738
"""

def loadCSV(filename):
	rows = []
	try:
		with open(filename) as csvfile:
			readCSV = csv.reader(csvfile, delimiter=',')
			rows = [row for row in readCSV]
			
			return rows
	except FileNotFoundError:
		msg = "Can't find file {0}.".format(filename)
		print(msg)


def groupNames(rows):
	"""
	Groups rows together by same name.
	"""
	names = []
	groups = defaultdict(list)
	for row in rows:
		name = row[0]
		if name not in names:
			names.append(name)
		groups[name].append(row)
	return (names, groups)

def removeDupes(names, groups):
	"""
	Returns a list of rows without duplicates.
	"""
	newCSV = []
	for name in names:
		newCSV.append(mostComplete(groups[name]))
	return newCSV
		
def mostComplete(rows):
	"""
	Returns a list with the most non-empty elements.
	"""
	max = []
	for row in rows:
		if countColumns(row) > countColumns(max):
			max = row
	return max
				
def countColumns(row):
	return len([i for i in row if i])
	
def saveCSV(header, newCSV, filename):
	try:
		with open(filename, 'w', newline='') as csvfile:
			row_writer = csv.writer(csvfile)
			row_writer.writerow(header)
			for row in newCSV:
				row_writer.writerow(row)
	except FileNotFoundError:
		msg = "Can't find file {0}.".format(filename)
		print(msg)
	
if __name__ == "__main__":

	print("Enter the name of the csv file.")

	filename = input()
	
	rows = loadCSV(filename)
	header = rows[0]
	group_tuple = groupNames(rows[1:])
	
	namelist = group_tuple[0]
	groups = group_tuple[1]
	newCSV = removeDupes(namelist, groups)
	filename = 'dupetest.csv'
	saveCSV(header, newCSV, filename)
	