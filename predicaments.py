# predicaments.py
# generates the dictionary that holds all the available predicaments
# home to doIf() and getNonBlankLine()
# also the new home of the Predicament class

from savedata import *
from funtoolkit import *
from settings import *
from errors import errors

class BadPredicamentError(Exception):
    def __init__(self, code=0, *args):
        print("\nerror code:", code)
        if code != 0 and code < len(errors):
            print(errors[code] % args)
        print("i can't work under these conditions. i quit.\n")
        quit()

class Predicament:
    """this is a class for holding a predicament!
when creating a Predicament, pass in a string holding the name.
the constructor will try to find this pred's data in the preddir
by checking the predicaments dictionary.
to play this predicament, call its play() method
"""

    # class variable, accessible anywhere, shared by instances of Predicament
    numPredicaments = 0

    def __init__(self, name):
        Predicament.numPredicaments += 1
        self.name = name
        self.text = []
        self.setvars = []
        # 99% of objects will have a disable at some point, because we append
        # 'redraw' at the end of initial execution. this stops it from
        # being redrawn when the user unpauses, backspaces, etc.
        self.disable = []
        self.actions = []
        # self.goto is a list if inputtype == 'normal', a string otherwise
        self.goto = []
        self.inputtype = None
        self.result = None
        self.prompt = None
        self.sound = []
        self.write = None
        self.predmap = None
        self.mapname = None
        # self.directions contains a list of lists
        # in the format of [label, destination]
        # this is inconsistent with the way we handle action destinations. v_v
        self.directions = [0, 0, 0, 0] # up, down, left, right

        try:
            filename, lineNo = predicaments[self.name]
            open(preddir + filename, 'r')
        except KeyError:
            # if the predicament isn't in our master dictionary...
            raise BadPredicamentError(3, self.name)
        except:
            # if the file can't be opened...
            raise BadPredicamentError(15, filename, self.name)
        busy = False # whether we are currently reading a predicament
        with open(preddir + filename, 'r') as fp:
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
            global readingIfLevel, tempIfLevel
            readingIfLevel = 0
            tempIfLevel = 0
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
                elif line.strip().startswith("if "):
                    if doIf(fp, self.name, line):
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
                    continue
                elif line.strip().startswith("set "):
                    try:
                        key, value = line.split('to')
                    except ValueError:
                        try:
                            key, value = line.split('=')
                        except ValueError:
                            raise BadPredicamentError(31, filename, self.name,
                                                      line)
                    # strip out the 'set ' part
                    key = key[4:].strip()
                    value = value.strip()
                    try:
                        # split on first space to get dictionary
                        dictionary, key = key.split(' ', 1)
                    except ValueError:
                        # if there's no space, assume profile
                        dictionary = 'profile'
                    if dictionary not in ('quest', 'profile'):
                        raise BadPredicamentError(30, filename, self.name, line,
                                                  dictionary)
                    if dictionary == 'quest':
                        dictionary = 'quests'
                        if value == 'done':
                            value = True
                        elif value == 'not done':
                            value = False
                        else:
                            raise BadPredicamentError(32, filename, self.name,
                                                      line, value)
                    # store it as a list of tuples (dictionary, variable, value)
                    if dictionary == 'profile':
                        try:
                            if (value == 'random' and
                                type(profile[key.strip()]) == int):
                                self.setvars.append(('profile', key.strip(),
                                                     random.randint(1,100)))
                                continue
                        except KeyError:
                            # nonexistant variable
                            raise BadPredicamentError(21, self.name, dictionary,
                                                      key.strip())
                    self.setvars.append((dictionary, key.strip(), value))
                    continue
                elif line.strip().startswith("give "):
                    item = line[5:].strip()
                    if item in items:
                        self.setvars.append(('items', item, True))
                    else:
                        raise BadPredicamentError(33, filename, self.name,
                                                  'give', item)
                    continue
                elif line.strip().startswith("take "):
                    item = line[5:].strip()
                    if item == 'a pack of ketchup':
                        # don't even THINK about it
                        raise BadPredicamentError(34, filename, self.name)
                    if item in items:
                        self.setvars.append(('items', item, False))
                    else:
                        raise BadPredicamentError(33, filename, self.name,
                                                  'take', item)
                    continue
                try:
                    key, value = line.split('=')
                except ValueError:
                    raise BadPredicamentError(18, filename, self.name, line)
                key = key.rstrip().lower()
                if key == 'new predicament':
                    # we're in a new predicament without closing the last one.
                    # the pred file must be invalid.
                    raise BadPredicamentError(4, filename, self.name)
                elif key in ('text', 'yell', 'cyan'):
                    # remove only the first space if any.
                    # leading whitespace is now allowed!
                    if value and value[0] == ' ':
                        value = value[1:]
                    # add each line of text onto the prev line of text
                    if styleCode and key != 'text':
                        if key == 'yell':
                            line = styleCode['bold']
                        elif key == 'cyan':
                            line = styleCode['cyan']
                        line += value + styleCode['reset']
                        self.text.append(line)
                    else:
                        self.text.append(value)
                elif key == 'action':
                    # we only allow abcdef - 6 actions
                    if len(self.actions) < 6 and len(self.goto) < 6:
                        try:
                            action, goto = value.split('->')
                        except ValueError:
                            raise BadPredicamentError(23, self.name, line)
                        self.actions.append(action.strip())
                        self.goto.append(goto.strip())
                elif key == 'disable':
                    # i don't want smart-alecs assigning this directly
                    if value.strip() != 'redraw':
                        self.disable.append(value.strip())
                elif key == 'sound':
                    self.sound.append(value.strip())
                elif key == 'goto':
                    self.goto = value.strip()
                elif key == 'type':
                    if value.strip() not in ('none', 'normal', 'input',
                                             'skip', 'multiline', 'technical'):
                        raise BadPredicamentError(6, filename, self.name,
                                                  value.strip())
                    self.inputtype = value.strip()
                elif key == 'result':
                    self.result = value.strip()
                elif key == 'prompt':
                    self.prompt = value.strip()
                elif key == 'write':
                    self.write = value.strip()
                elif key == 'map':
                    self.predmap = value.strip()
                elif key == 'name':
                    self.mapname = value.strip()
                elif key in ('up', 'down', 'left', 'right'):
                    try:
                        label, goto = value.split('->')
                    except ValueError:
                        raise BadPredicamentError(23, self.name, line)
                    if key == 'up':
                        self.directions[0] = [label.strip(), goto.strip()]
                    elif key == 'down':
                        self.directions[1] = [label.strip(), goto.strip()]
                    elif key == 'left':
                        self.directions[2] = [label.strip(), goto.strip()]
                    elif key == 'right':
                        self.directions[3] = [label.strip(), goto.strip()]
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
        # if the map is 'none', there's literally no map
        # if it's merely unspecified, assume it's the last map loaded
        if not self.predmap:
            self.predmap = profile['latestPredmap']
            self.mapname = profile['latestMapname']
        else:
            profile['latestPredmap'] = self.predmap
            profile['latestMapname'] = self.mapname

    # this isn't used anywhere, but handy for debugging
    def __str__(self):
        return 'Predicament: %s: %s' % (self.name, self.text)

    # allows user to make a choice, returns their choice as a string
    # separated into two functions to make pre- and post- actions easier
    def play(self):
        clear()
        if self.inputtype != 'technical':
            profile['predicament'] = self.name
        # if there are SET statements in predicament,
        # do those before printing text
        if self.setvars:
            for statement in self.setvars:
                # make tuple readable
                dictionary, variable, value = (statement[0], statement[1],
                                               statement[2])
                if dictionary == 'profile':
                    try:
                        if type(profile[variable]) == int:
                            profile[variable] = int(value)
                        else:
                            profile[variable] = value
                    except KeyError:
                        # nonexistent variable
                        raise BadPredicamentError(21, self.name, dictionary,
                                                  variable)
                    except ValueError:
                        # tried to set an int to a string
                        raise BadPredicamentError(20, self.name, variable,
                                                  value, variable)
                if dictionary == 'quests':
                    if variable in quests:
                        quests[variable] = value
                    else:
                        raise BadPredicamentError(21, self.name, dictionary,
                                                  variable)
                if dictionary == 'items':
                    if variable in items:
                        items[variable] = value
                    else:
                        raise BadPredicamentError(21, self.name, dictionary,
                                                  variable)
        # draw the map
        if self.predmap != 'none':
            try:
                self.drawMap()
            except FileNotFoundError:
                raise BadPredicamentError(22, self.name, self.predmap, mapdir)
        # try playing sounds if they work and exist
        if playSound and self.sound and 'redraw' not in self.disable:
            for sound in self.sound:
                soundPlayed = playSound(sound)
            if not soundPlayed:
                raise BadPredicamentError(19, self.name, sound)
        if 'animation' in self.disable and 'redraw' not in self.disable:
            self.disable.append('redraw')
        # use extraDelay to give bigger blocks of text longer pauses
        self.extraDelay = 0
        # prevent player from barfing on the text (by hiding their input)
        with PreventBarfing():
            for line in self.text:
                if 'redraw' in self.disable:
                    print(replaceVariables(line))
                else:
                    self.extraDelay = fancyPrint(line, self.extraDelay)
            # print a newline after things which don't
            # have more options to print
            if self.inputtype != 'normal':
                self.extraDelay = fancyPrint('', self.extraDelay)
        # decide what the prompt will be
        if self.prompt:
            # if there is a custom prompt, just use it
            if not self.prompt.strip().startswith('['):
                self.prompt = "[" + self.prompt + "]"
        elif self.disable and "prompt" in self.disable:
            # otherwise, disable the prompt if it's disabled
            self.prompt = ""
        elif not self.disable or "prompt" not in self.disable:
            # or, just use the default prompt depending on inputtype
            if self.inputtype == 'normal':
                self.prompt = "\n[" + defaultNormalPrompt + "]"
            elif self.inputtype == 'input':
                self.prompt = "[" + defaultInputPrompt + "]"
            elif self.inputtype == 'multiline':
                self.prompt = "[" + defaultMultilinePrompt + "]"
            else:
                self.prompt = "[" + defaultNonePrompt + "]"
        # once we're done fancyprinting, we don't want to redraw the
        # predicament if we return to it after unpausing, backspacing, etc
        if 'redraw' not in self.disable and self.inputtype != "normal":
            # but normal predicaments still have some fancyprinting to do
            self.disable.append('redraw')
        result = self.getPlayerInput()
        if self.write:
            with open('funtimes.out', 'a') as output:
                if type(profile[self.write]) is list:
                    for line in profile[self.write]:
                        output.write(line + '\n')
                else:
                    output.write(profile[self.write] + '\n')
        return result

    # allows user to make a choice, returns their choice as a string
    # this bit only handles the different inputtypes
    def getPlayerInput(self):
        if self.disable and 'pause' in self.disable:
            canPause = False
        else:
            canPause = True
        if self.inputtype == 'skip':
            return self.goto
        elif self.inputtype == 'none':
            ch = anykey(self.prompt)
            if commonOptions(ch, canPause):
                return self.name
            # hit backspace or ^H to go back
            elif ch == '\x08' or ch == '\x7F':
                return '\x7F'
            # hit ^R to forcibly redraw the text
            elif ch == '\x12':
                self.disable.remove('redraw')
                return self.name
            return self.goto
        elif self.inputtype == 'technical':
            ch = anykey(self.prompt)
            if commonOptions(ch, canPause):
                return self.name
            if ch == 'n':
                print("Are you sure you want to start a new game? [Y/N]")
                print("This will overwrite your current save file!")
                ch = 'x'
                while ch not in ('y', 'n'):
                    ch = anykey()
                if ch == 'n':
                    return self.name
                if ch == 'y':
                    save(True) # reset save.dat to defaults
                    load()
                    return self.goto
            return profile['predicament']
        elif self.inputtype == 'input':
            print(self.prompt)
            # flush terminal input so nothing gets prefixed to this value
            sys.stdout.flush()
            tcflush()
            profile[self.result] = input().strip()
            while profile[self.result] == '':
                # print the last line of text till valid input is provided
                profile[self.result] = input(self.prompt + "\n").strip()
            return self.goto
        elif self.inputtype == 'multiline':
            print(self.prompt)
            try:
                sys.stdout.flush()
                termios.tcflush(sys.stdin, termios.TCIOFLUSH)
                profile[self.result] = []
                words = ''
                while True:
                    words = input().strip()
                    profile[self.result].append(words)
            except EOFError:
                return self.goto
        elif self.inputtype == 'normal':
            actions = actionButtons[:len(self.actions)]
            iteractions = iter(actions)
            # prevent player from barfing on text (by hiding their input)
            with PreventBarfing():
                fancyPrint('', self.extraDelay)
                for direction in self.directions:
                    if type(direction) == list:
                        string = (' ' + arrows[self.directions.index(direction)]
                                  + '  - ' + direction[0])
                        if 'redraw' in self.disable:
                            print(string)
                        else:
                            fancyPrint(string, -1)
                for action in self.actions:
                    string = ' ' + next(iteractions) + '  - ' + action
                    if 'redraw' in self.disable:
                        print(string)
                    else:
                        fancyPrint(string, -1)
            # *now* normal predicaments are done fancyprinting
            self.disable.append('redraw')
            choice = anykey(self.prompt)
            while True:
                if commonOptions(choice, canPause):
                    return self.name
                # hit backspace or ^H to go back
                elif choice == '\x08' or choice == '\x7F':
                    return '\x7F'
                # hit ^R to forcibly redraw the text
                elif choice == '\x12':
                    self.disable.remove('redraw')
                    return self.name
                elif choice in movementButtons:
                    # if the corresponding direction exists, return it
                    if self.directions[0] and choice == movementButtons[0]:
                        return self.directions[0][1]
                    elif self.directions[1] and choice == movementButtons[1]:
                        return self.directions[1][1]
                    elif self.directions[2] and choice == movementButtons[2]:
                        return self.directions[2][1]
                    elif self.directions[3] and choice == movementButtons[3]:
                        return self.directions[3][1]
                    else:
                        choice = anykey(self.prompt)
                elif choice not in actions:
                    choice = anykey(self.prompt)
                else:
                    return self.goto[actions.index(choice)]

    def drawMap(self):
        with open(mapdir + self.predmap + '.map',
                  'r', encoding='utf-8') as currentMap:
            # find out the longest line so we can centre according to it
            longestLine = 0
            for line in currentMap:
                if len(line) > longestLine:
                    longestLine = len(line)
        with open(mapdir + self.predmap + '.map',
                  'r', encoding='utf-8') as currentMap:
            # print the map's name over the map if it exists
            if self.mapname:
                # centre it over the map
                sys.stdout.write \
                (' ' * int((lineLength - len(self.mapname) - 1) / 2))
                print(self.mapname.upper())
            for line in currentMap:
                sys.stdout.write(' ' * int((lineLength - longestLine) / 2))
                try:
                    print(line, end='')
                except UnicodeEncodeError:
                    # if the terminal does not support unicode,
                    # replace fancy unicode walls with ascii walls
                    unicodeCharacters = ['\u2550', '\u2551', '\u2554',
                                         '\u2557', '\u255A', '\u255D']
                    for character in unicodeCharacters:
                        line = line.replace(character, '#')
                    print(line, end='')
            print()

def doIf(fp, name, line):
    # figures out whether to read conditional stuff in pred definitions
    # first, parse the line itself to get dictionary, key, and value

    global tempIfLevel, readingIfLevel

    # try splitting the if on 'is' or 'has' or '='
    # nested trys are ugly, we could maybe do something better
    try:
        key, value = line.split('is')
    except ValueError:
        try:
            key, value = line.split('has')
        except ValueError:
            try:
                key, value = line.split('=')
            except ValueError:
                raise BadPredicamentError(26, fp.name, name, line)
    # remove the 'if ' from the key
    key = key[3:].strip()
    value = value.strip()
    tempIfLevel = readingIfLevel + 1
    # now, try to split key to determine dictionary & real key
    try:
        dictionary, key = key.split()
    except ValueError:
        if key == 'player':
            # 'if player has item'
            dictionary = 'items'
            key = value
            value = True
            # results in 'if items['item'] == True'
        else:
            # if it's anything else, assume profile
            dictionary = 'profile'
    if dictionary == 'items' and key.startswith('not '):
        # 'if player has not item'
        key = key[4:].strip()
        value = False
    if dictionary == 'quest':
        dictionary = 'quests'
        if value == 'done':
            value = True
        elif value == 'not done':
            value = False
        else:
            raise BadPredicamentError(27, fp.name, name, line)
    if dictionary not in ('profile', 'quests', 'items'):
        raise BadPredicamentError(28, fp.name, name, line, dictionary)
    if (dictionary == 'profile' and key not in profile or
        dictionary == 'quests' and key not in quests or
        dictionary == 'items' and key not in items):
        raise BadPredicamentError(10, fp.name, name, line, key, dictionary)

    followup = getNonBlankLine(fp).lower() # get 'then', 'and', 'or'

    # profile comparison cases
    if dictionary == 'profile':
        if value.startswith('>') or value.startswith('<'):
            if type(profile[key]) not in (int, float):
                # the key in profile isn't a comparable type
                raise BadPredicamentError(24, fp.name, name, line, key)
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
                    raise BadPredicamentError(25, fp.name, name, line,
                                              key, value[1:].strip())
            if value[1:].strip() in dir():
            #if value[1:].strip() in dir(__name__):
                # uh oh. a consequence of using eval...
                # the pred file can refer to variables in this code
                # this doesn't even catch all of these cases
                # it might, if we hadn't called something else predicaments
                raise BadPredicamentError(96)
            if type(comparee) not in (int, float):
                # the value isn't a comparable type
                raise BadPredicamentError(25, fp.name, name, value,
                                          profile[key], comparee)
            if value.startswith('>'):
                conditionIsTrue = ( profile[key] > comparee )
            if value.startswith('<'):
                conditionIsTrue = ( profile[key] < comparee )
        else:
            negate = False
            if value.startswith('not '):
                value = value[4:] # remove the 'not ' part
                negate = True
            if value.startswith('<') or value.startswith('>'):
                # can't be arsed supporting negated comparisons
                raise BadPredicamentError(29, fp.name, name, line)
            if type(profile[key]) == int:
                try:
                    conditionIsTrue = ( profile[key] == int(value) )
                except ValueError:
                    if (value in profile and
                        type(profile[value]) in (int, float)):
                            conditionIsTrue = \
                                         ( profile[key] == int(profile[value]) )
                    else:
                        raise BadPredicamentError(25, fp.name, name,
                                                  line, key, value)
            else:
                if value in profile:
                    conditionIsTrue = ( profile[key] == profile[value] )
                else:
                    conditionIsTrue = ( profile[key] == value )
            if negate:
                conditionIsTrue = not conditionIsTrue

    if dictionary == 'items':
        conditionIsTrue = ( items[key] == value)

    if dictionary == 'quests':
        conditionIsTrue = ( quests[key] == value )

    if followup.startswith("then not"):
        # don't use this, it breaks if more than one statement is processed
        # for the simplest statements, it's okay.
        return not conditionIsTrue
    elif followup.startswith("then"):
        return conditionIsTrue
    line = getNonBlankLine(fp)
    if not line.startswith("if "):
        raise BadPredicamentError(11, fp.name, name, "'%s'" % followup)
    if followup.startswith("and not"):
        return ( not doIf(fp, name, line) and conditionIsTrue )
    elif followup.startswith("and"):
        return ( doIf(fp, name, line) and conditionIsTrue )
    elif followup.startswith("or not"):
        return ( not doIf(fp, name, line) or conditionIsTrue )
    elif followup.startswith("or"):
        return ( doIf(fp, name, line) or conditionIsTrue )
    raise BadPredicamentError(11, fp.name, name, line)

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
def findPredicaments(preddir):
    if not os.path.isdir(preddir):
        raise BadPredicamentError(8)
    predicaments = {}
    for filename in os.listdir(preddir):
        basename, ext = os.path.splitext(filename)
        if ext != '.pred':
            print("WARNING: skipping %s/%s%s..." % (preddir, basename, ext))
            continue
        pointless = True # whether this boolean is pointless
        lineNo = 0
        with open(preddir + filename, 'r') as fp:
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

preddir = os.getcwd() + '/data/predicaments/'
mapdir = os.getcwd() + '/data/maps/'
predicaments = findPredicaments(preddir)

if __name__ == '__main__':
    print("content of", preddir, ": ", os.listdir(preddir))
    print()
    print("number of predicaments:", len(predicaments))
    for key in predicaments:
        print(key + ":", predicaments[key])
    print('making first predicament')
    a = Predicament('title')
    a.play()
    print("\nnow raising BadPredicamentError:")
    raise BadPredicamentError(0)

