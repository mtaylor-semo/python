#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from docxtpl import DocxTemplate, RichText
from collections import defaultdict
import re

tmpl=DocxTemplate('annual_report_tmpl.docx')

# If report is generated in December, then use current
# year. Otherwise, assume it is January of the the year the
# report is due so subtract 1 to get information for the year
# of the annual report.

if datetime.now().month == 12:
	theYear = datetime.now().year
else: 
	theYear = datetime.now().year-1


# Dictionary with all bean categories, all set to 'N/A'
# final_dict = dict.fromkeys(\
# 	['IA3',\
# 	'IB1','IB2','IB3','IB4','IB5','IB6','IB7','IB8',\
# 	'IC1','IC2','IC3','IC4','IC5','IC6','IC7','IC8','IC9','IC10',\
# 	'IIA1','IIA2','IIA3','IIA4','IIA5','IIA6','IIA7',\
# 	'IIB1','IIB2','IIB3','IIB4','IIB5','IIB6','IIB7','IIB8','IIB9','IIB10','IIB11','IIB12',\
# 	'IIC1','IIC2','IIC3',\
# 	'IIIA1','IIIA2','IIIA3','IIIA4','IIIA5','IIIA6','IIIA7','IIIA8','IIIA9','IIIA10',\
# 	'IIIB1','IIIB2','IIIB3','IIIB4','IIIB5','IIIB6','IIIB7','IIIB8','IIIB9','IIIB10','IIIB11','IIIB12'], [RichText('N/A')])

final_dict = defaultdict(list)
for roman in ('I','II','III'):
	for letter in ('A','B','C'):
		for num in xrange(1,13):
			bean_category = str(roman + letter + str(num))
			final_dict[bean_category] = [RichText('N/A')]

## Latex Bold and italics regex commands.
## Leaves bf{ and it{ for conversion to
## proper docx formats.
latexbfit = re.compile(r'\\text([bfitsc]{2}\{[a-zA-Z0-9 .?()]+)\}')
latexnewline = re.compile(r'\\newline.*\\newline[ ]?')
latexdollar = re.compile(r'\\\$')
latexmedskip = re.compile(r'\\medskip')
latexsmallcap = re.compile(r'\\textsc{([a-z]{2})}')

## Strip out latex commands, replacing with RichText for bold and italics.
#  Add more as necessary.
def strip_latex( beanlist ):
	"""Function to remove latex commands.
	Replaces \newline with \n. 
	Replaces \$ with $.
	Reduces \textbf and \textit to bf{ and it{
	for replacement with docx commands."""
	beanlist = re.sub('\\\,','',beanlist) # Latex thinspace \,
	beanlist = re.sub('~',' ', beanlist)  # Latex fixed space ~
	beanlist = re.sub(latexnewline, '\n\n', beanlist)
	beanlist = re.sub(latexdollar, '$', beanlist)
	beanlist = re.sub(latexmedskip,"",beanlist)
	beanlist = re.sub(latexsmallcap, lambda m: m.group(1).upper(),beanlist)

	
	# Add code to remove other commands.
	x = re.split(latexbfit, beanlist)
	rt = RichText("")
	l = len(x)
	for i in range(0,l):
		if x[i].startswith('bf{'):
			rt.add(x[i][3:], bold=True)
		elif x[i].startswith('it{'):
			rt.add(x[i][3:], italic=True)
		elif x[i].startswith('sc{'):
			rt.add(x[i][3:], italic=True)
		else:
		    rt.add(x[i])
	return rt

## Open the file
basename = "dossier_beans.txt"
with open(basename) as f:
	contents = f.read().splitlines()

## Convert lines to dictionary.
bean_dict = defaultdict(list)

data_list = [lines.split("\t") for lines in contents if not lines.startswith('#')]

for line in data_list:

	bean = line[0]

	if line[1] == 'N/A':
		bean_dict[bean].append(RichText('N/A'))
	elif 'AY'+str(theYear+1) in line[1] or line[1] == str(theYear):
#	if 'AY'+str(theYear+1) in line[1] or line[1] == str(theYear):
		if len(line[2:]) > 1:
			myBean = str(line[2]) + '\n\n' + str(line[3]) + '\n'
		else:
			myBean = str(line[2])
	
		myBean = strip_latex(myBean)

		bean_dict[bean].append(myBean)

#	The subheading lines (e.g., course names, internships, readings, etc.)
#	These have an empty string for the year, but text in the third position.
	elif not line[1] and line[2]:
		myBean = line[2]
		myBean = strip_latex(myBean)

		bean_dict[bean].append(myBean)


## Replace the N/A entries in the final_dict with entries
## from the bean_dict
final_dict.update(bean_dict)

## Add the current year to the dictionary for the report year.
final_dict['reportyear'] = theYear

## Render the final Word document.
tmpl.render(final_dict)
tmpl.save('annual_report.docx')
