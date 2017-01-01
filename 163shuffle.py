#!/usr/bin/env python

import re, os, codecs
from random import shuffle

def index_containing_substring(the_list, substring):
    for i, s in enumerate(the_list):
        if substring in s:
              return i
    return -1

version_lett = ["A", "B", "C"] #Will produce versions A, B, C

############################
## Shuffle the Matching file
############################
name_of_file = 'matching' #Is substituted with sed from the script (no manual editing required)

# Open tex file and read its text
fmatch = codecs.open("matching.tex",'r','utf-8')
data = fmatch.read()

for j in range(0,len(version_lett)):
    data_v = re.sub("Version xx","Version " + version_lett[j],data) #Put version letter
    x_problems = re.findall(r'(\\question.*?)\n',data_v,re.DOTALL) #List with problems
    version_file = codecs.open(os.getcwd() + "/" + str(name_of_file) + str(version_lett[j]) + ".tex", 'w+','utf-8') #Create tex file to write to
    shuffle(x_problems) #Shuffle the problems
    version_file.write("\\bumppoints{"+str(len(x_problems)*2)+"}\n")
    for l in range(0,len(x_problems)):
        version_file.write(x_problems[l]+"\n\n")
        version_file.write("\\vspace{1\\baselineskip}" + "\n\n")
fmatch.close()

################################
## Shuffle the Multi Choice file
################################

name_of_file = 'multiplechoice'

# Open tex file and read its text
fmulti = codecs.open("multiplechoice.tex",'r','utf-8')
data = fmulti.read()

for j in range(0,len(version_lett)):
    data_v = re.sub("Version xx","Version " + version_lett[j],data) #Put version letter
    x_problems = re.findall(r'(%BeginMC.*?%EndMC)',data_v,re.DOTALL) #List with problems
    version_file = codecs.open(os.getcwd() + "/" + str(name_of_file) + str(version_lett[j]) + ".tex", 'w+','utf-8') #Create tex file to write to

#    version_file.write("%!TEX encoding = UTF-8 Unicode\n\n")

    version_file.write("\\bumppoints{"+str(len(x_problems)*2)+"}\n")
    shuffle(x_problems) #Shuffle the problems

    for k in range(0,len(x_problems)):
        not_to_shuffle = [] #List where answers that do not get shuffled will be put
        pos_unshuffled = [] #List where position of answers that do not get shuffled will be put
        x_answers_all_aux = []
        x_answers_all = re.findall(r'(\\[coret]*?choice.*?)%EndChoice',x_problems[k],re.DOTALL) #List with answers of k-th problem
        not_to_shuffle = [x for x in x_answers_all if "%dontshuffle" in x]
        if len(not_to_shuffle) > 0:
            x_answers_all_aux = x_answers_all
            for n in range(0,len(not_to_shuffle)):
                pos_unshuffled.append(index_containing_substring(x_answers_all_aux, "%dontshuffle") + n)
                x_answers_all_aux.remove(not_to_shuffle[n])
            x_answers_all_aux = []
            x_answers = [x for x in x_answers_all if x not in not_to_shuffle]
        else:
            x_answers = x_answers_all
        shuffle(x_answers) #Shuffle the answers to k-th problem
        if len(not_to_shuffle) > 0:
            for n in range(0,len(not_to_shuffle)):
                x_answers.insert(pos_unshuffled[n], not_to_shuffle[n])


        # We allow for two types of lists, one with horizontal and one with vertical spacing
        if re.search(r'\\begin{choices}',x_problems[k],re.DOTALL) is not None:
            x_problem_statement = re.findall(r'%BeginMC(.*?)\\begin{choices}',x_problems[k],re.DOTALL) #Problem statement (no answers included)
            version_file.write(x_problem_statement[0]) #Write problem statement
            version_file.write("\\begin{choices}\n") #Write \benumi in order to start possible answers (horizontal spacing)
            for l in range(0,len(x_answers)):
                version_file.write(x_answers[l]+"\n") #Write possible answers
            x_end_problem_statement = re.findall(r'(\\end{choices}.*?)%EndMC',x_problems[k],re.DOTALL) #Problem statement (no answers included)
            version_file.write(x_end_problem_statement[0]) #Write the last part of the problem after the answers
        else:
            x_problem_statement = re.findall(r'%BeginMC(.*?)\\begin{choices}',x_problems[k],re.DOTALL) #Problem statement (no answers included)
            version_file.write(x_problem_statement[0]) #Write problem statement
            version_file.write("\\begin{choices}\n") #Write \benum in order to start possible answers (vertical spacing)
            for l in range(0,len(x_answers)):
                version_file.write(x_answers[l]+"\n") #Write possible answers
            version_file.write("\\end{choices}\n\n") #Write \eenum\ep to end the problem
fmulti.close()

##############################
## Shuffle the True False file
##############################

name_of_file = 'truefalse' #Is substituted with sed from the script (no manual editing required)

# Open tex file and read its text
fTrueFalse = open("truefalse.tex",'r')
data = fTrueFalse.read()

for j in range(0,len(version_lett)):
    data_v = re.sub("Version xx","Version " + version_lett[j],data) #Put version letter
    x_problems = re.findall(r'(\\question.*?)\n',data_v,re.DOTALL) #List with problems
    version_file = open(os.getcwd() + "/" + str(name_of_file) + str(version_lett[j]) + ".tex", 'w+') #Create tex file to write to
    shuffle(x_problems) #Shuffle the problems
    version_file.write("\\bumppoints{"+str(len(x_problems)*2)+"}\n")
    for l in range(0,len(x_problems)):
	    version_file.write(x_problems[l]+"\n")
fTrueFalse.close()
	    
