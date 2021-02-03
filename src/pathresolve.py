class RelPathInavlid(Exception):
    """Raised when the relative path is invalid"""
    pass

def resolvePathUNIX(abs, rel):
    newPath = ''
    if rel[0:2] == './':
        newPath = abs + rel[1:]
    elif rel[0:3] == '../':
        absSegs = abs.split("/")
        relSegs = rel.split("/")
        backLevels = sum(x == ".." for x in relSegs)
        if backLevels >= len(absSegs):
            raise RelPathInavlid
        newPathArr = absSegs[1:(backLevels * -1)]
        for relLevel in relSegs:
            if relLevel != '..':
                newPathArr.append(relLevel)
        for lvl in newPathArr:
            newPath = newPath + '/' + lvl
    else:
        raise RelPathInavlid

    return newPath