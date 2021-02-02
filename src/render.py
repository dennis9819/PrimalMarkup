import pyfiglet

def renderSeperator(properties):
    outString = ''

    for i in range(0, properties['Document']['defaultWidth']):
        outString = "{}{}".format(outString, properties['Document']['spacerChar'])
    
    return outString

def renderHeader(properties):
    ascii_banner = pyfiglet.figlet_format(properties['Document']['shorttitle'])
    ascii_banner = "{}Title   :   {}".format(ascii_banner,properties['Document']['title'])
    ascii_banner = "{}\nAuthor  :   {}\n".format(ascii_banner,properties['Document']['author'])
    return ascii_banner

def repeatChar(symbol, amount):
    outString = ''
    for i in range(0, int(amount)):
        outString = "{}{}".format(outString, symbol)
    return outString

def renderSectionTitle(properties, title):
    titleString = "{}. {}".format(properties['counter_section'] ,title)
    titleLen = len(titleString)
    return "{}\n{}".format(titleString, repeatChar('=', titleLen))

def renderSubsectionTitle(properties, title):
    titleString = "{}.{} {}".format(properties['counter_section'] ,properties['counter_subsection'] ,title)
    titleLen = len(titleString)
    return "{}{}\n{}{}".format(properties['Document']['indentation'],titleString, properties['Document']['indentation'], repeatChar('-', titleLen))

def renderContentTable(properties, content):
    contentString = ''

    for section in content:
        sectionNumber = section['number']
        titleString = "{}. {}".format(sectionNumber, section['title'])
        titleStringLen = len(titleString)
        contentString = "{}\n{}\n{}".format(contentString,titleString,repeatChar('-',titleStringLen))
        
        #subsections
  
        for subsection in section['subsections']:
            titleString = "{}.{} {}".format(sectionNumber,subsection['number'], subsection['title'])
            contentString = "{}\n{}{}".format(contentString,properties['Document']['indentation'],titleString)
        
        contentString = "{}\n".format(contentString)


    return contentString[1:]