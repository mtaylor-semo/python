#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import print_function

import re
import string

# Dictionary that contains each of the achievements
# for each of the three main categories:
# Teaching (I), Professional Development (II), and Service (III).
IAdict = \
	{0: "Student feedback on teaching performance. This may include departmental or nationally normed student evaluation data, or other evidence of students' views.",\
	 1: "Peer evaluation of teaching performance. (Required for non-tenured faculty; optional for tenured faculty.)",\
	 2: "Other documentation of teaching performance (optional)."}

IBdict = \
	{0: "Major revision of existing courses.",\
	 1: "New course development.",\
	 2: "Program development.",
	 3:	"Obtaining internal funding, or applying for or obtaining external funding, for the improvement of teaching.",\
	 4: "Pedagogical, \\textbf{peer-reviewed} publication. (Note: A specific achievement may be included here or under Professional Growth, but not both.)",\
     5: "Including students in research, with appropriate justification of level of effort. (Note: a specific achievement may be listed here or under section \\textsc{ii.b.10}, but not both)",\
	 6: "Conducting readings, independent study, internships, etc., with appropriate justification of level of effort.",\
	 7: "Other, as documented and justified as to level of effort."}

ICdict = \
	{0: "Attendance/participation in organized activities that contribute directly or indirectly to course improvement.",\
	 1: "Development/incorporation of new course materials as necessary to enhance learning experiences for students.",\
	 2: "Development/improvement of teaching techniques as necessary to enhance learning experiences for students.",\
	 3: "Participation in organized activities that contribute directly or indirectly to improvement in teaching techniques.",\
	 4: "Applying for internal funding for the improvement of teaching.",\
	 5: "Pedagogical presentation or non peer-reviewed publication. (A specific achievement may be included here or under Professional Growth, but not both.)",\
     6: "Including students in research. (Note: a specific achievement may be listed here or under section \\textsc{ii.b.10}, but not both.)",\
	 7: "Conducting readings, independent study, internships.",\
     8: "Sharing teaching expertise with faculty and teaching assistants. (Note: a specific achievement may be listed here or under section \\textsc{iii.b.9}, but not both.)",\
	 9: "Other, as documented."}

IIAdict = \
    {0: "Publication of \\textbf{peer-reviewed} original scholarly work in a journal, electronic journal, web site, book, or book chapter. See Supporting Material \\textsc{ii.a.1}.",\
     1: "Publication of a \\textbf{peer-reviewed} literature review of original research in a journal, electronic journal, web site, book, or book chapter. See Supporting Material \\textsc{ii.a.2}.",\
	 2: "Publication of a \\textbf{peer-reviewed} textbook chapter, text-related web site, or ancillary materials.",\
	 3: "Receipt of external funding to support scholarly work (this includes external contracts).",\
	 4:	"Scholarly work in progress (as documented by narrative with appropriate justification of level of effort).",\
	 5: "Recognized national/international reputation in the discipline (e.g., as evaluated by national or international peers through letters of recommendation, citations by others in the field, etc.).",\
	 6: "Other, as documented and justified as to level of effort."}

IIBdict = \
    {0: "Presentation of original scholarly work at professional meetings. See Supporting Material \\textsc{ii.b.1}.",\
	 1: "Invited presentations at other institutions or professional meetings.",\
     2: "Publication/preparation of technical reports. See Supporting Material \\textsc{ii.b.3}.",\
	 3: "Publication of non-peer reviewed articles, book reviews, or book chapters.",\
	 4: "Publication of manuals, brochures, web pages, etc.",\
	 5: "Production or maintenance of public databases.",\
	 6:	"Peer-review of journals, books, book chapters or grants.",\
	 7: "Internal funding received to support scholarly work.",\
	 8: "External funding applied for, but not received.",\
     9: "Participation in graduate or undergraduate student scholarly work. (Note: a specific achievement may be listed here or under section \\textsc{i.b.6} or \\textsc{i.c.7}, but not both.)",\
	 10: "Contribution to public scholarly databases (e.g., GenBank).",\
	 11: "Other, as documented."}

IICdict = \
	{0: "Advanced study at other institutions.",\
	 1: "Participation in workshops and institutes.",\
	 2: "Other, as documented."}

IIIAdict = \
	{0: "Leadership on college committees.",\
	 1: "Leadership on university committees.",\
	 2: "Leadership on departmental committees.",\
	 3: "Membership on the executive committee of faculty senate.",\
	 4: "Participation on departmental committees beyond normal expectations with appropriate justification as to level of effort.",\
	 5: "Receipt of grants in support of institutional programs.",\
	 6: "Leadership in professional organizations.",\
	 7: "Advising in excess of a normal load.",\
	 8: "Other service to the university (e.g., but not limited to: reviews, report writing, service on task forces, additional service assignments).",\
	 9: "Other, as documented and justified as to level of effort."}

IIIBdict = \
	{0: "Participation on college committees.",\
	 1: "Participation on university committees.",\
	 2: "Membership in faculty senate.",\
	 3: "Participation on committees of candidates for advanced degrees. This does not include supervision of graduate student research.",\
	 4: "Sponsorship of student organizations.",\
	 5: "Representation of the Department in support of either on- or off-campus activities that promote the University.",\
	 6: "Submission and/or receipt of grants in support of institutional programs.",\
	 7: "Contributions to interdisciplinary programs.",\
     8: "Sharing expertise with other faculty members. (Note: a specific achievement may be listed here or under section \\textsc{i.c.9}, but not both.)",\
	 9: "Service to the region that utilizes his/her professional expertise.",\
	 10: "Supportive participation in professional organizations.",\
	 11: "Other, as documented. (Non-tenure track faculty may include items from section II, Professional Growth, which pertain to service in a broad context)."}

# Print section IA. This section must be handled differently
# from all other sections due to dossier requirements.

def print_section_ia(secName, dictName):

    # Number of entries in IA dictionary.
    maxitem = len(dictName)

    outFile.write('\n\\begin{enumerate}\n')

    for m in range(0, maxitem):

        outFile.write('\\item ' + dictName[m])
        
        beans = [bean for bean in secName if int(bean[1]) == (m+1)]
        
        if m == 0:
            outFile.write('\n\input{evaluation_preamble}\n\n')
            # outFile.write('\n\input{evaluation_table_idea.tex}\n\n')
            outFile.write('\n\input{evaluation_table_smart.tex}\n\n')
            outFile.write('\input{narrative_reflective.tex}\n\n')
        else:
            if m == 1:
                outFile.write('\t\\begin{description}[font=\\normalfont]\n')
                outFile.write('\t\t\\item[N/A] Peer evaluation is not required for tenured faculty in my department.\n')

                outFile.write('\t\\end{description}\n\n')
            else:
                if not beans:
                    outFile.write('\t\\begin{description}[font=\\normalfont]\n')
                    outFile.write('\t\t\\item[N/A]\n')
                    outFile.write('\t\\end{description}\n\n')
                else:
                    # l = len(beans)
                    outFile.write('\t\\begin{description}[font=\\normalfont]\n')
                    for i in range(0, len(beans)):

                        outFile.write('\t\t\\item[\\small ' + beans[i][3] + '] ' + beans[i][4] + '\n')
                        if len(beans[i]) == 5:
                            print('length = 5\n')
                            outFile.write('\n\n\t\t' + beans[i][4] + '\n')

                    #outFile.write('\t\\end{description}\n\n')

    outFile.write('\\end{enumerate}\n')


def print_section(secName, dictName):
    """Print each section of the dossier, as necessary."""

    # Number of entries in IA dictionary.
    maxitem = len(dictName)

    outFile.write('\n\\begin{enumerate}\n')

    for m in range(0, maxitem):

        outFile.write('\\item ' + dictName[m])

        beans = [bean for bean in secName if int(bean[1]) == (m+1)]

        if beans[0][-1] == 'N/A':
            outFile.write('\n\t\\begin{description}[font=\\normalfont]\n')
            outFile.write('\t\t\\item[N/A]\n')
            outFile.write('\t\\end{description}\n\n')
        else:
            # l = len(beans)
            if beans[0][2].startswith('AY'):
                outFile.write('\n\t\\begin{description}[leftmargin=1.75cm, font=\\normalfont]\n')
                beans[0][2] = str.replace(beans[0][2], 'AY', '\\textsc{ay}')
            else:
                outFile.write('\n\t\\begin{description}[font=\\normalfont]\n')
            for i in range(0, len(beans)):
                if beans[i][2].startswith('AY'):
                    beans[i][2] = str.replace(beans[i][2], 'AY', '\\textsc{ay}')
                outFile.write('\t\t\\item[\\small ' + beans[i][2] + '] ' + beans[i][3] + '\n')

                if len(beans[i]) == 5:
                    outFile.write('\n\n\t\t' + beans[i][4] + '\n')

            outFile.write('\t\\end{description}\n\n')

    outFile.write('\\end{enumerate}\n')


InFileName = 'dossier_beans.txt'
with open(InFileName, 'r') as f:
    myFile = [line.strip('\n') for line in f if line.strip()]
    myBeans = [line.split('\t') for line in myFile if not line.startswith('#')]
f.close()

bean_len = len(myBeans)

for counter in range(0, bean_len):

    first_bean = re.split('([0-9]+)', myBeans[counter][0])
    
    myBeans[counter].remove(myBeans[counter][0])
    myBeans[counter].insert(0, first_bean[1])
    myBeans[counter].insert(0, first_bean[0])


sectionIA = [bean for bean in myBeans if (bean[0] == 'IA')]
sectionIB = [bean for bean in myBeans if (bean[0] == 'IB')]
sectionIC = [bean for bean in myBeans if (bean[0] == 'IC')]

sectionIIA = [bean for bean in myBeans if (bean[0] == 'IIA')]
sectionIIB = [bean for bean in myBeans if (bean[0] == 'IIB')]
sectionIIC = [bean for bean in myBeans if (bean[0] == 'IIC')]

sectionIIIA = [bean for bean in myBeans if (bean[0] == 'IIIA')]
sectionIIIB = [bean for bean in myBeans if (bean[0] == 'IIIB')]

# outFile = open('dossier_sections.tex','w')

outFile = open('dossier_teaching.tex', 'w')

# Begin Effective Teaching
outFile.write('\\MainSection{I: Teaching Effectiveness}\n\n')
outFile.write('\input{narrative_current.tex}\n\n')

outFile.write('\\SubSection{A: Teaching Performance}\n\n'),
outFile.write(
    '\\vspace{0.5\\baselineskip}\\hspace{0.5cm}The faculty member displays evidence of:\n\n')
print(sectionIC[1][0])
print_section_ia(sectionIA, IAdict)

outFile.write('\n\\SubSection{B: Significant Teaching Achievements}\n\n'),
outFile.write(
    '\\vspace{0.5\\baselineskip}\\hspace{0.5cm}The faculty member displays evidence of:\n\n')

print_section(sectionIB, IBdict)

outFile.write('\n\\SubSection{C: Teaching Achievements}\n\n',)
outFile.write(
    '\\vspace{0.5\\baselineskip}\\hspace{0.5cm}The faculty member displays evidence of:\n\n')

print_section(sectionIC, ICdict)

outFile.close()


# Begin Professional Development
outFile = open('dossier_professional.tex', 'w')

outFile.write('\MainSection{II: Professional Growth}\n\n')
outFile.write('\SubSection{A: Significant Scholarly Achievements}\n\n')
outFile.write(
    '\\vspace{0.5\\baselineskip}\\hspace{0.5cm}The faculty member displays evidence of:\n\n')
print_section(sectionIIA, IIAdict)

outFile.write('\n\\SubSection{B: Scholarly Achievements}\n\n')
outFile.write(
    '\\vspace{0.5\\baselineskip}\\hspace{0.5cm}The faculty member displays evidence of:\n\n')
print_section(sectionIIB, IIBdict)

outFile.write('\n\\SubSection{C: Continuing Education Achievements}\n\n')
outFile.write(
    '\\vspace{0.5\\baselineskip}\\hspace{0.5cm}The faculty member displays evidence of:\n\n')
print_section(sectionIIC, IICdict)

outFile.close()

# Begin Service
outFile = open('dossier_service.tex', 'w')

outFile.write('\\MainSection{III: Service}\n\n')
outFile.write(
    '\\SubSection{A: Significant Achievements in Governance or Service}\n\n')
outFile.write(
    '\\vspace{0.5\\baselineskip}\\hspace{0.5cm}The faculty member displays evidence of:\n\n')
print_section(sectionIIIA, IIIAdict)

outFile.write('\n\\SubSection{B: Achievements in Governance or Service}\n\n')
outFile.write(
    '\\vspace{0.5\\baselineskip}\\hspace{0.5cm}The faculty member displays evidence of:\n\n')
print_section(sectionIIIB, IIIBdict)

outFile.close()
