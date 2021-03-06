#!/usr/bin/python3
# funtoolkit.py
# this is where common methods are declared.
# pause, clear, load, save, help, stats, etc.

import os
import time
import sys
import random
from subprocess import call, DEVNULL

from savedata import profile, items, quests, prefs
from settings import fancyPrintSpeed, fancyPrintLineDelay, datadir, movementButtons

sounddir = os.getcwd() + '/data/sound/'

# define system-dependent features
if os.name == 'nt':
    call('title FUNTIMES',shell=True)
    call('color 5F',shell=True)
    styleCode = None

    def clear():
        if not prefs['clearOff']:
            call('cls',shell=True)

    if prefs['soundOff']:
        import winsound
        def playSound(sound):
            if not os.path.isdir(sounddir):
                return False
            try:
                error = winsound.PlaySound(sounddir + sound + '.wav',
                                           winsound.SND_FILENAME)
            except:
                return False
            return True
    else:
        playSound = None

    def anykey(message=''):
        if message:
            print(message)

        from msvcrt import getch
        # getch returns b'[character]', so we turn it into a string
        # and strip out the b' and ' parts
        while msvcrt.kbhit():
            char = getch()
        # some inputs need to be compared using their number, for some reason
        if ord(char) == 224:
            # aha! an arrow key!
            char = ord(getch())
            if char == 72:
                char = movementButtons[0] # up
            elif char == 80:
                char = movementButtons[1] # down
            elif char == 75:
                char = movementButtons[2] # left
            elif char == 77:
                char = movementButtons[3] # right
        elif ord(char) == 3:
            char = 'q' # KeyboardInterrupt
        elif ord(char) == 27:
            char = 'p' # Esc
        elif ord(char) == 8:
            char = '\x7F' # backspace
        elif ord(char) == 18:
            char = '\x12' # ctrl-R
        else:
            char = str(char)[2:-1]
        if char == 'q':
            quit(True)
        return char.lower()

    def quit(askToSave=False, message="See you!"):
        if askToSave:
            print("\nDo you want to save before quitting? [Y/N]")
            ch = 'x'
            while ch not in ('y','n'):
                ch = anykey().lower()
            if ch == 'y':
                save()
        # for some reason resetting doesn't work when you use call()?
        # so for now we'll just assume they're using the default 07
        call('color 07',shell=True)
        print("\n" + message)
        raise SystemExit

    class PreventBarfing:
        def __enter__(self):
            barf = True
        def __exit__(self, typ, value, callback):
            barf = False
            # there we go, barfing stopped

    def tcflush():
        # irrelevant in windows! :>
        pass

else: # anything but windows
    import termios
    # store terminal settings for restoration on quit()
    stdinfd = sys.stdin.fileno()
    oldtcattr = termios.tcgetattr(stdinfd)
    styleCode = {
        'bold' : "\x1b[1m",
        'cyan' : "\x1b[36m",
        'reset' : "\x1b[0m",
    }

    def clear():
        if not prefs['clearOff']:
            call('clear',shell=True)

    def makePlaySound(sound, ext='.wav'):
        print("Configuring sounds...")
        # find a good way to find available sound-playing commands
        players = ('paplay', 'aplay', 'mplayer')
        for playa in players:
            #print("trying playa: ", playa)
            try:
                exit = call([playa, sounddir + sound + ext],
                            stdout=DEVNULL, stderr=DEVNULL)
            except FileNotFoundError:
                # this program isn't installed, move on to the next one
                continue
            if exit == 0:
                #print('success with:', playa)
                break
        else:
            return None

        def playSound(sound):
            if not os.path.isdir(sounddir):
                return False
            try:
                # making this explicit since shell exits
                # go opposite of typical python booleans
                if call([playa, sounddir + sound + ext],
                        stdout=DEVNULL, stderr=DEVNULL) != 0:
                    return False
                return True
            except Exception as e:
                print('strange error playing sounds. i didnt test much\n', e)
                quit()
        return playSound

    # gotta restructure this to happen after load()
    if prefs['soundOff']:
        playSound = makePlaySound('test')
    else:
        playSound = None

    def quit(askToSave=False, message="See you!"):
        if askToSave:
            print("\nDo you want to save before quitting? [Y/N]")
            ch = 'x'
            while ch not in ('y','n', '\x03'):
                ch = anykey()
            if ch == 'y':
                save()
        print("\n" + styleCode['reset'] + message)
        # restore terminal to the way it was
        termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
        raise SystemExit

    import tty
    # allows user to press any key to continue. thanks, Matthew Adams:
    # http://stackoverflow.com/questions/11876618/python-press-any-key-to-exit
    def anykey(*messages):
        # a lot of this is already taken care of elsewhere
        # store stdin's file descriptor
        #stdinFileDesc = sys.stdin.fileno()
        # save stdin's tty attributes so I can reset it later
        #oldStdinTtyAttr = termios.tcgetattr(stdinFileDesc)
        for message in messages:
            print(message)
        try:
            # set the input mode of stdin so that it gets added to
            # char by char rather than line by line
            tty.setraw(stdinfd)
            # read 1 byte from stdin (indicating that a key has been pressed)
            char = sys.stdin.read(1)
        finally:
            # reset
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
        if char == '\x03' or char == 'q':
            #quit(True)
            # i keep trying to quit by hitting ^C twice
            # now i can! not pretty though HEH
            raise KeyboardInterrupt
        if char == '\x1b':
            # disabling this because it breaks ESC. seems hard to fix :/
            if False:
                # arrow keys return 3 bytes - \x1b, [, and a letter
                # we'll read the next 2 bytes so we know which arrow was pressed
                char = sys.stdin.read(2)
                if char == '[A': # up
                    char = movementButtons[0]
                elif char == '[B': # down
                    char = movementButtons[1]
                elif char == '[D': # left
                    char = movementButtons[2]
                elif char == '[C': # right
                    char = movementButtons[3]
        return char.lower() # ignore caps lock

    class PreventBarfing:
        # stops user from barfing on the text (by pressing keys during fancyPrint)
        def __enter__(self):
            newtcattr = oldtcattr[:]
            newtcattr[3] = newtcattr[3] & ~termios.ECHO
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, newtcattr)
        def __exit__(self, typ, value, callback):
            termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)

    def tcflush():
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

# method what replaces variables' plaintext representations
# with the actual variable
def replaceVariables(text):
    if '%' not in text or '%' not in text[text.index('%')+1:]:
        # '%' doesn't appear or doesn't appear again after appearing
        return text
    start = text.index('%')
    end = text[start+1:].index('%') + start + 1
    if text[start+1:end] not in profile:
        print("can't find %s in profile" % text[start+1:end])
        quit()
    return replaceVariables(text[:start] + str(profile[text[start+1:end]])
                            + text[end+1:])

def save(defaults=False, filename="save.dat"):
    try:
        with open(datadir + filename, 'w', encoding='utf-8') as savefile:
            if not defaults:
                print("profile:", file=savefile)
                for key in profile.keys():
                    #print("%s=%s" % (key, profile[key]), file=savefile)
                    print(key + "=" + str(profile[key]), file=savefile)
                print("items:", file=savefile)
                for key in items.keys():
                    if items[key] == True:
                        print(key, file=savefile)
                print("quests:", file=savefile)
                for key in quests.keys():
                    if quests[key] == True:
                        print(key, file=savefile)
                print("prefs:", file=savefile)
                for key in prefs.keys():
                    if prefs[key] == True:
                        print(key, file=savefile)
            else:
                with open(datadir+'profile.dat', 'r', encoding='utf-8') as fp:
                    for line in fp:
                        print(line, file=savefile, end='')
    except IOError:
        print("error saving data :(")
        quit()

def load(filename="save.dat"):
    try:
        with open(datadir + filename, 'r', encoding='utf-8') as savefile:
            # unset any true booleans
            global items, quests, prefs
            for dic in (items, quests, prefs):
                for key in dic:
                    if dic[key] == True:
                        dic[key] = False
            # reset the ones we actually want
            for line in savefile:
                line = line.strip()
                if line.endswith(':'):
                    try:
                        dic = eval(line[:-1])
                    except ValueError:
                        print("ValueError reading dictionary:", line)
                        quit()
                    except: # just in case i'm wrong
                        print("exception reading dictionary:", line)
                        quit()
                    #pass 
                    # i think you meant continue...
                    continue
                if dic not in (profile, items, quests, prefs):
                    # this should be unnecessary because of the earlier test
                    print("error: unknown dictionary...")
                    quit()
                if dic == profile:
                    try:
                        key, value = line.split('=')
                    except ValueError:
                        continue
                    if type(profile[key]) == int:
                        try:
                            profile[key] = int(value)
                        except ValueError:
                            continue
                    else:
                        profile[key] = value
                else:
                    if line in dic:
                        dic[line] = True
    except:
        # if save.dat is corrupt, invalid, or nonexistent, recreate it
        save(True)

def stats(pause=True):
    clear()
    print("CHARACTER STATS:")
    print("You are a %s named %s %s." % (profile['gender'],
          profile['firstname'], profile['lastname']))
    if profile['weet'] == 1:
        print("You currently have 1 weet point.")
    else:
        print("You currently have %d weet points." % profile['weet'])
    # format money number to be human-readable (add commas)
    money = format(profile['money'], ",d")
    print("You have $%s in your pocket." % money)
    if profile['energy'] == 1:
        print("You have 1 energy point left.")
    else:
        print("You have %d energy points left." % profile['energy'])
    if profile['strongth'] > 14:
        print("You are quite strong.")
    if profile['charisma'] > 14:
        print("You have a lot of charisma.")
    if profile['dexterity'] > 14:
        print("You are highly dextrous.")
    if profile['intellect'] > 14:
        print("You are very intelligent.")
    if profile['love'] == 2:
        print("You have a crush on %s" % profile['girlname'])
    elif profile['love'] == 3:
        print("You're dating %s" % profile['girlname'])
    elif profile['love'] == 4:
        print("You're in love with %s" % profile['girlname'])
    print("\nITEMS ON HAND:")
    for item in sorted(items):
        if items[item] == True:
            print(item)
    # if player has >20 items, tell them they have deep pockets
    if sum(items.values()) > 20: # true=1 so the sum of items' values=#ofItems
        print("absurdly deep pockets")
    if pause:
        anykey()

def pause():
    stats(pause=False)
    print("\nMash 's' to save, 'l' to load, " +
          "'q' to quaff potion--er, I mean quit")
    ch = anykey()
    # hit 'p' or escape to unpause
    if ch == 'p' or ch == '\x1B':
        return
    elif commonOptions(ch):
        return
    elif ch == 's':
        save()
        print("Your data is saved!")
        anykey()
        return
    elif ch == 'l':
        load()
        print("\nLoaded!")
        anykey()
        return

def commonOptions(ch, canPause=True):
    if canPause:
        # hit 'p' or escape to pause
        if ch == 'p' or ch == '\x1B':
            pause()
            return True
    if ch == 'h':
        helpme()
        return True
    return False

def helpme():
    clear()
    print('''You move around the world using the WSAD keys and perform actions
by pressing 1-6. In some cases, the game may ask for text input, after which
you must press enter. At any time, you can 'pause' with ESC to see your
inventory, stats, etc. or use backspace to undo an action. Use S and L while
paused to save and load your progress, and Q to quit. Use of this game while
intoxicated may be illegal in some jurisdictions.''')
    anykey()

def fancyPrint(text, extraDelay):
    # prints lines character-by-character to be fancy
    # uses extraDelay to pause longer after bigger blocks of text
    # pass in -1 as extraDelay to force a standard pause
    text = replaceVariables(text)
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(fancyPrintSpeed)
        if extraDelay > 0:
            # subtle difference between long lines and short ones
            extraDelay += fancyPrintSpeed
    if text == '':
        # use extraDelay to give bigger blocks of text longer pauses
        time.sleep(fancyPrintLineDelay*extraDelay)
        extraDelay = 0
    elif extraDelay < 0:
        # force a standard pause
        time.sleep(fancyPrintLineDelay)
    else:
        extraDelay += fancyPrintLineDelay
    print() # put a newline at the end
    return extraDelay


if __name__ == '__main__':
    savedata = load()
    profile = savedata[0]
    items = savedata[1]
    quests = savedata[2]
    print(replaceVariables("name is: %firstname%."))
    #save(savedata)
    #data = load()
    #print(data)
    while anykey("press any key to continue...") != 'q':
        pass
    helpme()
    stats(profile, items)
