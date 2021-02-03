# GuniaMarkup (Primal Markup Language)
import re
import sys
sys.path.append("./")
from render import *
import pyfiglet
import time
import uuid
import sys, getopt, os
from pathresolve import resolvePathUNIX
from pathlib import Path

#### VARS

gmuSettings_global = {
    'Document' : {
        'defaultWidth': '80',
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
gmuOutputFileTmp1 = "/tmp/{}.pmc1".format(tmpFileUUID)
gmuOutputFileTmp2 = "/tmp/{}.pmc2".format(tmpFileUUID)
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



def processFilePhase1(path, depth):
    
    startTime = time.time()
    print("[Phase 1] Processing PrimalMarkupScript-Sourcefile: {}".format(path))

    tempFile = open(gmuOutputFileTmp1, 'w')

    linkedFileCount = 0

    def processFile(path, depth, tempFile, linkedFileCount):
        try:
            linkedFileCount += 1
            inFile = open(path, 'r')
            inFileLines = inFile.readlines()

            lineCount = 0
            for line in inFileLines:
                lineCount += 1

                if line[0:6] == "{{gmu.":
                    # found content-tag
                    tagData = contenttagRegEx.match(line)
        
                    if not tagData:
                        abortParseError(lineCount, line, "Cannot parse content-tag")
                    
                    tagType = tagData.group(1)[4:]

                    if tagType == 'include':
                        filePath = os.path.dirname(path)
                        absPath = resolvePathUNIX(filePath, tagData.group(3))
                        print("[LINKING] Include {}".format(filePath))
                        # resolve filename in relation to current file
                        processFile(absPath , depth + 1, tempFile , linkedFileCount)
                        tempFile.write('\n')
                        continue
                
                tempFile.write(line)
        except IOError:
            abortParseError(lineCount,path,"Sourcefile not accessible")

    processFile(path, 0, tempFile, linkedFileCount)

    tempFile.close()
    endTime = time.time()

    print("[Phase 1] Linked {} lines in {}s".format(linkedFileCount, (endTime - startTime)))
    #print("          => Registered {} Sections".format(gmuSettings_global['counter_section']))
    print("          => Generated pmc-file {}".format(gmuOutputFileTmp1))



def processFilePhase2(path):
    try:
        startTime = time.time()
        print("[Phase 2] Processing PrimalMarkupScript-Sourcefile: " + path)

        inFile = open(path, 'r')
        inFileLines = inFile.readlines()
        tempFile = open(gmuOutputFileTmp2, 'w')

        lineCount = 0
        for line in inFileLines:
            lineCount += 1
            processLine(lineCount, line.strip(), tempFile)

        tempFile.close()
        endTime = time.time()

        print("[Phase 2] Compiled {} lines in {}s".format(lineCount, (endTime - startTime)))
        print("          => Registered {} Sections".format(gmuSettings_global['counter_section']))
        print("          => Generated pmc-file {}".format(gmuOutputFileTmp2))
    except IOError:
        print("Sourcefile not accessible")



def processFilePhase3(path):
    try:
        startTime = time.time()
        print("[Phase 3] Processing pmc1-file: " + path)

        inFile = open(path, 'r')
        inFileLines = inFile.readlines()
        tempFile = open(gmuOutputFile, 'w')

        lineCount = 0
        for line in inFileLines:
            lineCount += 1
            processLine2(lineCount, line[:-1], tempFile)

        tempFile.close()  
        endTime = time.time()

        print("[Phase 3] Generated Content-Table in {}s".format((endTime - startTime)))
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
        gmuInputFile = Path(current_value).resolve()
    elif current_argument in ("-h", "--help"):
        print ("Specify Input with -i or --input")
        print ("Specify Output with -o or --output")
        exit(0)
    elif current_argument in ("-o", "--output"):
        gmuOutputFile = Path(current_value).resolve()

if gmuInputFile == '':
    print("[ERROR] You need to specify an input file")
    exit(2)

if gmuOutputFile == '':
    print("[ERROR] You need to specify an output file")
    exit(2)

#check if files exist

processFilePhase1(gmuInputFile,0)
processFilePhase2(gmuOutputFileTmp1)
processFilePhase3(gmuOutputFileTmp2)

print("\nDone! Compiled 1 File.")