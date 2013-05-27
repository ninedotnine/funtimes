# predicaments.py
# generates the dictionary that holds all the available predicaments

import os
 
# this is temporary. find a better way to do it.
# allow the user to set in-game, if possible...
preferredButtons = 'abcdef'
#preferredButtons = '123456'
#preferredButtons = 'aoeujk'

predicaments = {}

datadir = os.getcwd() + '/data/predicaments'

if not os.path.isdir(datadir):
    #os.makedirs(datadir)
    print("error: no data directory")
    raise SystemExit

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
                # 'title of predicament' : ('which .pred file it is in',lineNo)
                name = name.strip()
                predicaments[name] = (filename, lineNo)

class Predicament:
    """this is a class for holding a predicament!"""

    # class variable, accessible anywhere, shared by instances of Predicament
    numPredicaments = 0

    def __init__(self, name):
        Predicament.numPredicaments += 1
        self.name = name
        self.text = None
        self.setvars = None
        self.options = None
        self.choices = None
        self.next = None
        self.inputtype = None
        self.result = None

        filename, lineNo = predicaments[name]
        fp = open(datadir + '/' + filename, 'r')
        busy = False #whether we are currently reading a predicament
        for line in fp:
            # count down to the correct line
            if lineNo > 1:
                lineNo -= 1
                continue
            line = line.strip()
            # skip blank lines and lines starting with '#'
            if line == '' or line[:1] == '#': 
                continue
            if not busy:
                #if line.find('new predicament') == 0:
                value = line.split('=')[1].strip()
                #key = key.strip()
                currentPredicament = value.strip()
                # if it's the right predicament, start parsing
                if currentPredicament == name:
                    busy = True
                    continue
            # if busy == True:
            else:
                if line.find("end of predicament") == 0:
                    busy = False
                    return
                key, value = line.split('=')
                key = key.strip()
                if key == 'new predicament':
                    # we're in a new predicament without closing the last one.
                    # the .pred file must be invalid.
                    print("error reading %s." % filename)
                    print(currentPredicament + " was not ended correctly.")
                    print("this is a fatal error. aborting")
                    raise SystemExit
                elif key == 'text':
                    if not self.text:
                        self.text = []
                    # add each line of text onto the prev line of text
                    self.text.append(value.strip())
                elif key == 'option':
                    if not self.options:
                        self.options = []
                    # we only allow abcdef - 6 options
                    if len(self.options) < 6:
                        self.options.append(value.strip())
                elif key == 'choice':
                    if not self.choices:
                        self.choices = []
                    # we only allow abcdef - 6 choices
                    if len(self.choices) < 6:
                        self.choices.append(value.strip())
                elif key[:3] == 'set':
                    if not self.setvars:
                        self.setvars = []
                    # everything between 'set' and '=' is the parameter
                    key, parameter = key.split() # parameter cannot have spaces in it
                    # stored as a list of tuples (variable, value)
                    self.setvars.append((parameter.strip(), value.strip()))
                elif key == 'next':
                    self.next = value.strip()
                elif key == 'inputtype':
                    self.inputtype = value.strip()
                elif key == 'result':
                    self.result = value.strip()
                else:
                    print("%s is not a valid pred directive" % key)
                    raise SystemExit
        fp.close()
        return

    #def __str__(self):
    #    return 'Predicament: %s: %s' % (self.name, self.text)


if __name__ == '__main__':
    #print("content of", datadir, ": ", os.listdir(datadir))
    #print()
    #print("number of predicaments:", Predicament.numPredicaments)
    print("number of predicaments:", len(predicaments))
    print("predicaments is:")
    for key in predicaments:
        print(key + ":", predicaments[key])
