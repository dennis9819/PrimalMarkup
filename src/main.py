# GuniaMarkup (Primal Markup Language)
import re
import sys
sys.path.append("./")
from render import *
import pyfiglet
import time
import uuid
import sys, getopt

#### VARS

gmuSettings_global = {
    'Document' : {
        'defaultWidth': 80,
        'doctype': 'info',
        'spacerChar': '#',
        'headerPrefix': 'False',
        'indentation': '\t'
    },
    'counter_section': 0,
    'counter_subsection': 0
}

content = []

tmpFileUUID = str(uuid.uuid4())

gmuInputFile = ''
gmuOutputFile = ''
gmuOutputFileTmp = "/tmp/{}.pmc1".format(tmpFileUUID)
currentScope = "Document"

metatagRegEx = re.compile('^\[\[([\w\d._]*)\=([\w\d\-\":;,._$%&\/\\\ ]*)\]\]$', re.IGNORECASE)
contenttagRegEx = re.compile('^\{\{([\w\d._]*)(\=([\w\d\-\":;,._$%&\/\\\ ]*))?\}\}$', re.IGNORECASE)

#### FUNCTIONS

def abortParseError(lineNumber, lineContent, errorMessage):
    print ("[ERROR] Parsing error in line {}".format(lineNumber))
    print ("> {}".format(lineContent))
    print ("  ===> {}".format(errorMessage))
    exit(1)

def processLine(lineNumber, lineContent, tempFile):
    #print("[DEBUG] Line{}: {}".format(lineNumber, lineContent))

    if len(lineContent) > 8:
        
        if lineContent[0:6] == "[[gmu.":
            # found meta-tag
            # pares tag
            tagData = metatagRegEx.match(lineContent)
   
            if not tagData:
                abortParseError(lineNumber, lineContent, "Cannot parse meta-tag")
                
            gmuSettings_global[currentScope][tagData.group(1)[4:]] = tagData.group(2)
            return
         

        if lineContent[0:6] == "{{gmu.":
            # found content-tag
            tagData = contenttagRegEx.match(lineContent)
   
            if not tagData:
                abortParseError(lineNumber, lineContent, "Cannot parse content-tag")
            
            tagType = tagData.group(1)[4:]

            if tagType == 'header':
                tempFile.write(renderHeader(gmuSettings_global) + '\n')
                return
            if tagType == 'seperator':
                tempFile.write(renderSeperator(gmuSettings_global) + '\n')
                return
            if tagType == 'section':
                gmuSettings_global['counter_section'] += 1
                gmuSettings_global['counter_subsection'] = 0

                content.append({
                    'title': tagData.group(3),
                    'number': gmuSettings_global['counter_section'],
                    'subsections': []
                })

                tempFile.write(renderSectionTitle(gmuSettings_global, tagData.group(3)) + '\n')
                return
            if tagType == 'subsection':
                
                gmuSettings_global['counter_subsection'] += 1
                content[gmuSettings_global['counter_section'] - 1]['subsections'].append({
                    'title': tagData.group(3),
                    'number': gmuSettings_global['counter_subsection'],
                })

                tempFile.write(renderSubsectionTitle(gmuSettings_global, tagData.group(3)) + '\n')
                return

            if tagType == 'contents':
                tempFile.write('{{gmu.contents}}\n')
            return
        
        if lineContent[0:2] == "%%":
            return

    tempFile.write(lineContent + '\n')

def processLine2(lineNumber, lineContent, tempFile):
    #print("[DEBUG] Line{}: {}".format(lineNumber, lineContent))

    if len(lineContent) > 8:

        if lineContent[0:6] == "{{gmu.":
            # found content-tag
            tagData = contenttagRegEx.match(lineContent)
   
            if not tagData:
                abortParseError(lineNumber, lineContent, "Cannot parse content-tag")
            
            tagType = tagData.group(1)[4:]

            if tagType == 'contents':
                tempFile.write(renderContentTable(gmuSettings_global, content ) + '\n')
                return
        
        if lineContent[0:2] == "%%":
            return

    tempFile.write(lineContent + '\n')


def processFile(path):
    try:
        startTime = time.time()
        print("[Phase 1] Processing PrimalMarkupScript-Sourcefile: " + path)

        inFile = open(path, 'r')
        inFileLines = inFile.readlines()
        tempFile = open(gmuOutputFileTmp, 'w')

        lineCount = 0
        for line in inFileLines:
            lineCount += 1
            processLine(lineCount, line.strip(), tempFile)

        tempFile.close()
        endTime = time.time()

        print("[Phase 1] Compiled {} lines in {}s".format(lineCount, (endTime - startTime)))
        print("          => Registered {} Sections".format(gmuSettings_global['counter_section']))
        print("          => Generated pmc1-file {}".format(gmuOutputFileTmp))
    except IOError:
        print("Sourcefile not accessible")



def processFileRound2(path):
    try:
        startTime = time.time()
        print("[Phase 2] Processing pmc1-file: " + path)

        inFile = open(path, 'r')
        inFileLines = inFile.readlines()
        tempFile = open(gmuOutputFile, 'w')

        lineCount = 0
        for line in inFileLines:
            lineCount += 1
            processLine2(lineCount, line[:-1], tempFile)

        tempFile.close()  
        endTime = time.time()

        print("[Phase 2] Generated Content-Table in {}s".format((endTime - startTime)))
        print("          => Generated info-file {}".format(gmuOutputFile))
    except IOError:
        print("Sourcefile not accessible")

def printHeader():
    print(pyfiglet.figlet_format("PrimalMarkup"))
    print("PrimalMarkupScript Compiler v1.0.0")
    print("(c)2021 - Dennis Gunia - dennisgunia.de\n")


#### EVALUATE PARAMETERS


full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

short_options = "ho:i:"
long_options = ["help", "output=", "input="]

try:
    arguments, values = getopt.getopt(argument_list, short_options, long_options)
except getopt.error as err:
    print (str(err))
    sys.exit(2)


#### MAIN
printHeader()


for current_argument, current_value in arguments:
    if current_argument in ("-i", "--input"):
        gmuInputFile = current_value
    elif current_argument in ("-h", "--help"):
        print ("Specify Input with -i or --input")
        print ("Specify Output with -o or --output")
        exit(0)
    elif current_argument in ("-o", "--output"):
        gmuOutputFile = current_value

if gmuInputFile == '':
    print("[ERROR] You need to specify an input file")
    exit(2)

if gmuOutputFile == '':
    print("[ERROR] You need to specify an output file")
    exit(2)

#check if files exist

processFile(gmuInputFile)
processFileRound2(gmuOutputFileTmp)

print("\nDone! Compiled 1 File.")