# stuffthatusedtobeinpredicaments.py
# generates the dictionary that holds all the available predicaments
# home to doIf() and getNonBlankLine()

import os
from profiledata import profile
 
predicaments = {}

datadir = os.getcwd() + '/data/predicaments'
if not os.path.isdir(datadir):
    raise BadPredicamentError(8)

def doIf(fp, parameter, value, name, filename):
    # figures out whether to read conditional stuff in pred definitions
    if parameter not in profile:
        raise BadPredicamentError(10, parameter)
    followup = getNonBlankLine(fp).lower()
    conditionIsTrue = ( profile[parameter] == value.strip() )
    if followup.startswith("then not"):
        # don't use this, it breaks if more than one statement is processed
        # for the simplest statements, it's okay. 
        return not conditionIsTrue
    elif followup.startswith("then"):
        return conditionIsTrue
    line = getNonBlankLine(fp)
    if not line.startswith("if "):
        raise BadPredicamentError(11, filename, name, "'%s'" % followup)
    key, value = line.split('=')
    parameter = key.split()[1].strip()
    if followup.startswith("and not"):
        return ( not doIf(fp, parameter, value) and conditionIsTrue )
    elif followup.startswith("and"):
        return ( doIf(fp, parameter, value) and conditionIsTrue )
    elif followup.startswith("or not"):
        return ( not doIf(fp, parameter, value) or conditionIsTrue )
    elif followup.startswith("or"):
        return ( doIf(fp, parameter, value) or conditionIsTrue )
    raise BadPredicamentError(11, filename, name, '%s = %s' % (parameter, value))

def getNonBlankLine(fp):
    line = ''
    while line == '' or line.startswith("#"):
        line = fp.readline()
        if not line:
            # if eof is reached, that's bad. 
            raise BadPredicamentError(17)
        line = line.strip()
    return line

# populate predicaments dictionary with locations of all known predicaments
for filename in os.listdir(datadir):
    basename, ext = os.path.splitext(filename)
    if ext != '.pred':
        print("WARNING: skipping %s/%s%s..." % (datadir, basename, ext))
        continue
    busy = False # whether we're currently reading a predicament
    lineNo = 0
    with open(datadir + '/' + filename, 'r') as fp:
        for line in fp:
            lineNo += 1
            line = line.strip()
            if line.find("new predicament") == 0:
                name = line.split('=')[1]
                # create entry in predicaments dictionary
                # 'title of predicament' : ('which pred file it is in',lineNo)
                name = name.strip()
                predicaments[name] = (filename, lineNo)

if __name__ == '__main__':
    print("content of", datadir, ": ", os.listdir(datadir))
    print()
    print("number of predicaments:", len(predicaments))
    for key in predicaments:
        print(key + ":", predicaments[key])
    print("\nnow raising BadPredicamentError:")
    raise BadPredicamentError(0)
