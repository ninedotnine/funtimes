# predicaments.py
# generates the dictionary that holds all the available predicaments
# home to doIf() and getNonBlankLine()
# also the new home of the Predicament class

import os 

from profiledata import profile
from funtoolkit import *
from settings import *
from errors import errors

class BadPredicamentError(Exception):
    def __init__(self, code=0, *args):
        print("\nerror code:", code)
        if code != 0 and code < len(errors):
            print(errors[code] % args) 
        print("i can't work under these conditions. i quit.\n")
        #raise SystemExit
        quit()

class Predicament:
    """this is a class for holding a predicament!
when creating a Predicament, pass in a string holding the name. 
the constructor will try to find this pred's data in the datadir
by checking the predicaments dictionary.
to play this predicament, call its play() method
"""

    # class variable, accessible anywhere, shared by instances of Predicament
    numPredicaments = 0

    def __init__(self, name):
        Predicament.numPredicaments += 1
        self.name = name
        self.text = None
        self.setvars = None
        # 99% of objects will have a disable at some point, because we append
        # 'fancytext' at the end of initial execution. this stops it from
        # being redrawn when the user unpauses, backspaces, etc. therefore
        # disable might as well be an existing list all the time
        self.disable = []
        self.options = None
        # goto is a list if inputtype = 'normal', a string otherwise 
        self.goto = None
        self.inputtype = None
        self.result = None
        self.prompt = None
        self.sound = None

        try:
            filename, lineNo = predicaments[self.name]
            open(datadir + '/' + filename, 'r')
        except KeyError:
            # if the predicament isn't in our master dictionary...
            raise BadPredicamentError(3, self.name)
        except:
            # if the file can't be opened...
            raise BadPredicamentError(15, filename, self.name)
        busy = False # whether we are currently reading a predicament
        with open(datadir + '/' + filename, 'r') as fp:
            # basically all of this is just to get to the right line and test
            for line in fp:
                # count down to the correct line
                if lineNo > 1:
                    lineNo -= 1
                    continue
                line = line.strip()
                # we know this is the right line, but check anyway!
                if line.find('new predicament') != 0:
                    raise BadPredicamentError(1, self.name)
                # if it's the wrong predicament, freak the hell out
                elif self.name != line.split('=')[1].strip():
                    raise BadPredicamentError(2, self.name)
                busy = True
                break
            if not busy:
                # we should be busy reading a predicament by this point...
                raise BadPredicamentError(5, filename, self.name)

            # finally, we start actually assigning the data
            # line should be true (it should still be the new pred line)
            readingIfLevel = 0
            while line:
                line = getNonBlankLine(fp)
                if line.find("end of predicament") == 0:
                    busy = False
                    break
                elif line.find("end if") == 0:
                    if readingIfLevel > 0:
                        readingIfLevel -= 1
                        continue
                    raise BadPredicamentError(12, filename, self.name)
                try:
                    key, value = line.split('=')
                except ValueError: 
                    raise BadPredicamentError(18, filename, self.name, line)
                key = key.rstrip().lower()
                if key == 'new predicament':
                    # we're in a new predicament without closing the last one.
                    # the pred file must be invalid.
                    raise BadPredicamentError(4, filename, self.name)
                elif key == 'text':
                    if not self.text:
                        self.text = []
                    # remove only the first space if any. 
                    # leading whitespace is now allowed!
                    if value and value[0] == ' ':
                        value = value[1:]
                    # add each line of text onto the prev line of text
                    self.text.append(value)
                elif key == 'option':
                    if not self.options:
                        self.options = []
                    # we only allow abcdef - 6 options
                    if len(self.options) < 6:
                        self.options.append(value.strip())
                elif key == 'choice':
                    if not self.goto:
                        self.goto = []
                    # we only allow abcdef - 6 choices
                    if len(self.goto) < 6:
                        self.goto.append(value.strip())
                elif key == 'disable':
                        self.disable.append(value.strip())
                elif key == 'sound':
                    if not self.sound:
                        self.sound = []
                    self.sound.append(value.strip())
                elif key.startswith("set "):
                    if not self.setvars:
                        self.setvars = []
                    # everything between 'set' and '=' is the parameter
                    # parameter cannot have spaces in it
                    key, parameter = key.split() 
                    # stored as a list of tuples (variable, value)
                    self.setvars.append((parameter.strip(), value.strip()))
                elif key == 'goto':
                    self.goto = value.strip()
                elif key == 'type':
                    if value.strip() not in ('none', 'normal', 'input', 'skip'):
                        raise BadPredicamentError(6, filename, self.name,
                                                  value.strip())
                    self.inputtype = value.strip()
                elif key == 'result':
                    self.result = value.strip()
                elif key == 'prompt':
                    self.prompt = value.strip()
                elif key.startswith("if "):
                    parameter = key.split()[1].strip()
                    tempIfLevel = readingIfLevel + 1
                    if doIf(fp, parameter, value.strip(), self.name):
                        # if the condition is true, read normally
                        readingIfLevel += 1
                        continue
                    # if the condition isn't true, 
                    # discard lines until we reach end if
                    while readingIfLevel < tempIfLevel:
                        nextline = getNonBlankLine(fp)
                        if nextline.startswith("end if"):
                            tempIfLevel -= 1
                        elif nextline.startswith("if "):
                            tempIfLevel += 1
                        elif nextline.find("end of predicament") == 0:
                            raise BadPredicamentError(13, self.name)
                else:
                    raise BadPredicamentError(14, filename, self.name, 
                                              key.strip())
                if not self.inputtype:
                    raise BadPredicamentError(16, filename, self.name)
        if readingIfLevel:
            raise BadPredicamentError(13, filename, self.name)
        elif busy:
            # should always hit error 4 before this, so it may be redundant
            raise BadPredicamentError(7, filename, self.name)

    # this isn't used anywhere, but handy for debugging
    def __str__(self):
        return 'Predicament: %s: %s' % (self.name, self.text)
    
    # allows user to make a choice, returns their choice as a string
    # should return a string
    def play(self):
        global profile, items, queststatus
        clear()
        # if there are SET statements in predicament, 
        # do those before printing text
        if self.setvars:
            for statement in self.setvars:
                # make tuple readable
                variable, value = statement[0], statement[1]
                try:
                    if type(profile[variable]) == int:
                        profile[variable] = int(value)
                    else:
                        profile[variable] = value
                except KeyError:
                    # nonexistent variable
                    raise BadPredicamentError(21, self.name, variable)
                except ValueError:
                    # tried to set an int to a string
                    raise BadPredicamentError(20, self.name, variable, value,
                                              variable)
        # try playing sounds if they work and exist
        #if profile['soundWorks']:
        if playSound and self.sound:
            for sound in self.sound:
                soundPlayed = playSound(sound)
            if not soundPlayed:
                raise BadPredicamentError(19, self.name, sound)
        # use extraDelay to give bigger blocks of text longer pauses
        extraDelay = 0
        # prevent player from barfing on the text (by hiding their input)
        newtcattr[3] = newtcattr[3] & ~termios.ECHO
        try:
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, newtcattr)
            for line in self.text:
                if "fancytext" in self.disable:
                    print(replaceVariables(line))
                else:
                    extraDelay = fancyPrint(line, extraDelay)
            # print a newline after things which don't have more options to print
            if self.inputtype != 'normal':
                extraDelay = fancyPrint('', extraDelay)
        finally:
            termios.tcsetattr(stdinfd, termios.TCSANOW, oldtcattr)
        # decide what the prompt will be
        if self.prompt:
            # if there is a custom prompt, just use it
            prompt = "[" + self.prompt + "]"
        elif self.disable and "prompt" in self.disable:
            # otherwise, disable the prompt if it's disabled
            prompt = ""
        elif not self.disable or "prompt" not in self.disable:
            # or, just use the default prompt depending on inputtype
            if self.inputtype == 'none':
                prompt = "[" + defaultNonePrompt + "]"
            elif self.inputtype == 'normal':
                prompt = "\n[" + defaultNormalPrompt + "]"
            elif self.inputtype == 'input':
                prompt = "[" + defaultInputPrompt + "]"
            elif self.inputtype == 'skip':
                prompt = "[" + defaultInputPrompt + "]"
        # once we're done fancyprinting, we don't want to redraw the 
        # predicament if we return to it while it's in memory 
        # (unpausing, using backspace, etc)
        if "fancytext" not in self.disable and self.inputtype != "normal":
            # but normal predicaments still have some fancyprinting to do
            self.disable.append("fancytext")
        if self.inputtype == 'none':
            ch = anykey(prompt)
            if commonOptions(ch):
                return self.name
            # hit backspace or ^H to go back
            elif ch == '\x08' or ch == '\x7F':
                return '\x7F'
            # hit ^R to forcibly redraw the text
            elif ch == '\x12':
                self.disable.remove("fancytext")
                return self.name
            return self.goto
        elif self.inputtype == 'skip':
            return self.goto
        elif self.inputtype == 'input':
            print(prompt)
            try:
                # flush terminal input so nothing gets prefixed to this value
                sys.stdout.flush()
                termios.tcflush(sys.stdin, TCIOFLUSH)
                profile[self.result] = input().strip()
                while profile[self.result] == '':
                    # print the last line of text till valid input is provided
                    profile[self.result] = input(prompt + "\n").strip()
            except KeyboardInterrupt:
                quit()
            return self.goto
        elif self.inputtype == 'normal':
            letters = preferredButtons[:len(self.options)]
            iterletters = iter(letters)
            # prevent player from barfing on text (by hiding their input)
            newtcattr[3] = newtcattr[3] & ~termios.ECHO
            try:
                termios.tcsetattr(stdinfd, termios.TCSADRAIN, newtcattr)
                fancyPrint('', extraDelay)
                for option in self.options:
                    string = next(iterletters) + ' - ' + option
                    if 'fancytext' in self.disable:
                        print(string)
                    else:
                        fancyPrint(string, -1)
            finally:
                termios.tcsetattr(stdinfd, termios.TCSANOW, oldtcattr)
            # *now* normal predicaments are done fancyprinting
            self.disable.append("fancytext")
            choice = anykey(prompt)
            while True:
                if commonOptions(choice):
                    return self.name
                # hit backspace or ^H to go back
                elif choice == '\x08' or choice == '\x7F':
                    return '\x7F'
                # hit ^R to forcibly redraw the text
                elif choice == '\x12':
                    self.disable.remove("fancytext")
                    return self.name
                elif choice not in letters:
                    choice = anykey(prompt)
                else:
                    return self.goto[letters.index(choice)]

def doIf(fp, parameter, value, name):
    # figures out whether to read conditional stuff in pred definitions
    if parameter not in profile:
        raise BadPredicamentError(10, parameter)
    followup = getNonBlankLine(fp).lower()

    # comparison cases
    if value.startswith('>') or value.startswith('<'):
        if type(profile[parameter]) not in (int, float):
            # the parameter in profile isn't a comparable type
            raise BadPredicamentError(99)
        try:
            comparee = eval(value[1:])
        except NameError:
            # it's not a comparable value.
            # maybe it's supposed to be a profile entry? 
            if ( value[1:].strip() in profile and 
                 type(profile[value[1:].strip()]) in (int, float) ):
                # aha! we're probably comparing profile stuff
                comparee = profile[value[1:].strip()] 
            else:
                raise BadPredicamentError(97)
        if value[1:].strip() in dir():
        #if value[1:].strip() in dir(__name__):
            # uh oh. a consequence of using eval...
            # the pred file can refer to variables in this code
            # this doesn't even catch all of these cases 
            # it might, if we hadn't called something else predicaments
            raise BadPredicamentError(96)
        if type(comparee) not in (int, float):
            # the value isn't a comparable type
            raise BadPredicamentError(98)
        if value.startswith('>'):
            conditionIsTrue = ( profile[parameter] > comparee )
        if value.startswith('<'):
            conditionIsTrue = ( profile[parameter] < comparee )
    else:
        conditionIsTrue = ( profile[parameter] == value.strip() )

    if followup.startswith("then not"):
        # don't use this, it breaks if more than one statement is processed
        # for the simplest statements, it's okay. 
        return not conditionIsTrue
    elif followup.startswith("then"):
        return conditionIsTrue
    line = getNonBlankLine(fp)
    if not line.startswith("if "):
        raise BadPredicamentError(11, fp.name, name, "'%s'" % followup)
    key, value = line.split('=')
    parameter = key.split()[1].strip()
    if followup.startswith("and not"):
        return ( not doIf(fp, parameter, value, name) and conditionIsTrue )
    elif followup.startswith("and"):
        return ( doIf(fp, parameter, value, name) and conditionIsTrue )
    elif followup.startswith("or not"):
        return ( not doIf(fp, parameter, value, name) or conditionIsTrue )
    elif followup.startswith("or"):
        return ( doIf(fp, parameter, value, name) or conditionIsTrue )
    raise BadPredicamentError(11, fp.name, name, '%s = %s' % (parameter, value))

def getNonBlankLine(fp):
    line = ''
    while line == '' or line.startswith("#"):
        line = fp.readline()
        if not line:
            # if eof is reached, that's bad. 
            raise BadPredicamentError(17, fp.name)
        line = line.strip()
    return line

# populate predicaments dictionary with locations of all known predicaments
def findPredicaments(datadir):
    if not os.path.isdir(datadir):
        raise BadPredicamentError(8)
    predicaments = {}
    for filename in os.listdir(datadir):
        basename, ext = os.path.splitext(filename)
        if ext != '.pred':
            print("WARNING: skipping %s/%s%s..." % (datadir, basename, ext))
            continue
        pointless = True # whether this boolean is pointless
        lineNo = 0
        with open(datadir + '/' + filename, 'r') as fp:
            for line in fp:
                lineNo += 1
                line = line.strip()
                if line.find("new predicament") == 0:
                    name = line.split('=')[1]
                    # create entry in predicaments dictionary
                    # 'title of predicament' : ('which pred file it is in',
                    #                         lineNo)
                    name = name.strip()
                    predicaments[name] = (filename, lineNo)
    return predicaments

datadir = os.getcwd() + '/data/predicaments'
predicaments = findPredicaments(datadir)

if __name__ == '__main__':
    print("content of", datadir, ": ", os.listdir(datadir))
    print()
    print("number of predicaments:", len(predicaments))
    for key in predicaments:
        print(key + ":", predicaments[key])
    print('making first predicament')
    a = Predicament('title')
    a.play()
    print("\nnow raising BadPredicamentError:")
    raise BadPredicamentError(0)

