''' Use the list of names from http://www.census.gov/genealogy/names/names_files.html to determine the gender of a given name
'''
import csv

#the format is name, frequency, cumulative frequency (useless), and rank 
_namesFcensus = [f for f in csv.reader(open('data/dist.female.first.txt'))]
_namesMcensus = [f for f in csv.reader(open('data/dist.male.first.txt'))]

# print(_namesFcensus) # Debugging
# print(_namesMcensus) # Debugging

# some pre-processing

for i in xrange(len(_namesFcensus)):
	row = _namesFcensus[i]
	row[0] = row[0].lower()
	row = row[0].split()
	row.append(0)
#	for j in xrange(len(_namesMcensus)): # Stuff for testing out M+F 
#		rowM = _namesMcensus[j]
#		rowM[0] = row[0].lower()
#		rowM = rowM[0].split()
#		if rowM[0] == row[0]:
#			row[4] = [0,1]
	_namesFcensus[i] = row
#	print row # Test

for i in xrange(len(_namesMcensus)):
	row = _namesMcensus[i]
	row[0] = row[0].lower()
	row = row[0].split()
	row.append(1)
	_namesMcensus[i] = row
#	print row # Test

'''for i in xrange(len(_namesFcensus)):
	rowF = _namesFcensus[i]
	for j in xrange(len(_namesMcensus)):
		rowM = _namesMcensus[j]
		if rowF[0] == rowM[0]:
			rowM[1] = [rowM[1], rowF[1]]
			rowM[2] = [rowM[2], rowF[2]]
			rowM[3] = [rowM[3], rowF[3]]
			rowM[4] = [0, 1]
			_namesMcensus[j] = rowM
			del _namesFcensus[i]
'''

# _namesCensus = [namesFcensus f if f not in namesMcensus]
_namesCensus = _namesFcensus + _namesMcensus
# print _namesCensus # Debugging

_threshold = 0.6

'''
# Example of name with multiple gender listing
for m in _namesMcensus:
	if m[0] == 'chris':
		print m

for n in _namesFcensus:
	if n[0] == 'chris':
		print n
'''

# print _names # Debugging

def gender(name):
	''' Return the gender of the given name, along with the difference in frequency (abs val)
	Possible gender return values are:
	MALE
	FEMALE
	NEUTRAL
	UNKNOWN
	e.g. fbnames.getGender('alex') returns ('MALE',0.91...)
	fbnames.getGender('julie') returns ('FEMALE',0.95...)
	'''
	name = name.lower()
	multipleGenders = []
	try:
		for n in _namesCensus:
			# need to deal with case of name in both lists... but for now:
			
			if n[0] == name: # case
				multipleGenders.append(n) # add to temp list
		if len(multipleGenders) >= 2:
			# This is when I decide
			# compare frequencies
			frequencyDiff = float(multipleGenders[0][1]) - float(multipleGenders[1][1]) # Female, then male
			if frequencyDiff > 0:
				return 'FEMALE', frequencyDiff
			elif frequencyDiff == 0:
				return 'NEUTRAL', frequencyDiff
			elif frequencyDiff < 0:
				return 'MALE', abs(frequencyDiff)
			else:
				return 'UNKNOWN', 0
		elif len(multipleGenders) == 1:
			if multipleGenders[0][4] == 0: # If this is a female listing
				return 'FEMALE', float(multipleGenders[0][1])
			elif multipleGenders[0][4] == 1: # If this is a male listing
				return 'MALE', float(multipleGenders[0][1])
			else: # Otherwise if there's some error in the data
				return 'UNKNOWN', float(multipleGenders[0][1])
		else:
			return 'UNKNOWN', 0
	except IndexError: 
		return 'broken?'

# print gender('Matthew') # Debugging
# print gender('Chris')
# print gender('Jacob')
# print gender('Fqhlal')
# print gender('Gina')
