#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from docxtpl import DocxTemplate, RichText
from collections import defaultdict
import re

tmpl = DocxTemplate('annual_report_tmpl.docx')

""" If report is generated in December, then use current
year. Otherwise, assume it is January of the the year the
report is due so subtract 1 to get information for the year
of the annual report.
"""

if datetime.now().month == 12:
    theYear = datetime.now().year
else:
    theYear = datetime.now().year-1

final_dict = defaultdict(list)
for roman in ('I', 'II', 'III'):
    for letter in ('A', 'B', 'C'):
        for num in range(1, 13):
            bean_category = str(roman + letter + str(num))
            final_dict[bean_category] = [RichText('N/A')]

""" Latex Bold and italics regex commands. Leaves bf{ and it{ for
conversion to proper docx formats.
"""
latexbfit = re.compile(r'\\text([bfitsc]{2}\{[a-zA-Z0-9 .?()]+)\}')
latexnewline = re.compile(r'\\newline.*\\newline[ ]?')
latexdollar = re.compile(r'\\\$')
latexmedskip = re.compile(r'\\medskip')
latexsmallcap = re.compile(r'\\textsc{([a-z]{2})}')


# Strip out latex commands, replacing with RichText for bold and italics.
# Add more as necessary.

def strip_latex(beanlist):

    """Function to remove latex commands.
    Replaces \newline with \n.
    Replaces \$ with $.
    Reduces \textbf and \textit to bf{ and it{
    for replacement with docx commands."""
    beanlist = re.sub('\\\,', '', beanlist)  # Latex thinspace \,
    beanlist = re.sub('~', ' ', beanlist)    # Latex fixed space ~
    beanlist = re.sub(latexnewline, '\n\n', beanlist)
    beanlist = re.sub(latexdollar, '$', beanlist)
    beanlist = re.sub(latexmedskip, "", beanlist)
    beanlist = re.sub(latexsmallcap, lambda m: m.group(1).upper(), beanlist)

    # Add code to remove other commands.
    x = re.split(latexbfit, beanlist)
    rt = RichText("")
#    l = len(x)
    for i in range(0, len(x)):
        if x[i].startswith('bf{'):
            rt.add(x[i][3:], bold=True)
        elif x[i].startswith('it{'):
            rt.add(x[i][3:], italic=True)
        elif x[i].startswith('sc{'):
            rt.add(x[i][3:], italic=True)
        else:
            rt.add(x[i])
    return rt


with open("dossier_beans.txt") as f:
    contents = f.read().splitlines()

# Convert lines to dictionary.
bean_dict = defaultdict(list)

data_list = [lines.split("\t") for
             lines in contents if not lines.startswith('#')]

for line in data_list:

    bean = line[0]

    if line[1] == 'N/A':
        bean_dict[bean].append(RichText('N/A'))
    elif 'AY' + str(theYear + 1) in line[1] or line[1] == str(theYear):
        if len(line[2:]) > 1:
            myBean = str(line[2]) + '\n\n' + str(line[3]) + '\n'
        else:
            myBean = str(line[2])

        myBean = strip_latex(myBean)
        bean_dict[bean].append(myBean)
    elif not line[1] and line[2]:
        myBean = line[2]
        myBean = strip_latex(myBean)

        bean_dict[bean].append(myBean)


""" Replace the N/A entries in the final_dict with entries
from the bean_dict
"""
final_dict.update(bean_dict)

# Add the current year to the dictionary for the report year.
final_dict['reportyear'] = theYear

# Render the final Word document.
tmpl.render(final_dict)
tmpl.save('annual_report.docx')
