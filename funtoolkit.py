#!/usr/bin/python3
# funtoolkit.py
# this is where common methods are declared.
# pause, clear, load, save, help, stats, etc. 

import os
import pickle
import time
import sys
import termios
from subprocess import call, DEVNULL

from profiledata import profile, items, queststatus
from settings import fancyPrintSpeed, fancyPrintLineDelay, soundOn, clearOn

sounddir = os.getcwd() + '/data/sound/'

# store terminal settings for restoration on quit()
stdinfd = sys.stdin.fileno()
oldtcattr = termios.tcgetattr(stdinfd)

# define system-dependent features
if os.name == 'nt':
    import winsound
    def clear():
        if clearOn:
            call('cls',shell=True)
    
    def playSound(sound):
        if not os.path.isdir(sounddir):
            return False
        try:
            error = winsound.PlaySound(sounddir + sound + '.wav',
                                       winsound.SND_FILENAME)
        except:
            return False
        return True

    # this makes testing in windows at least mildly possible for now
    # but obviously it doesn't work for 'normal' inputs, so it's rubbish
    def anykey(message=''):
        if message:
            print(message)
        call('pause >nul',shell=True)
        
    def initialize():
        call('title FUNTIMES',shell=True)
        call('color 5F',shell=True)
else: # anything but windows
    def clear():
        if clearOn:
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
            #if not profile['soundWorks']:
                #return True
            if not os.path.isdir(sounddir):
                return False
            try:
                # making this explicit since shell exits
                # go opposite of typical python booleans
                if call([playa, sounddir + sound + ext], 
                        stdout=DEVNULL, stderr=DEVNULL) != 0:
                    return False
                return True
            #except KeyboardInterrupt:
                #quit()
            except Exception as e:
                print('strange error playing sounds. i didnt test much\n', e)
                quit()
        return playSound

    if soundOn:
        playSound = makePlaySound('test')
    else:
        playSound = None

    def initialize():
        # nothing yet
        return

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
            #raise KeyboardInterrupt
            quit()
        return char

def save(filename="save.sav", pause=True):
    clear()
    savedata = (profile, items, queststatus)
    try: 
        with open(filename, 'wb') as savefile: 
            pickle.dump(savedata, savefile)
        print("your data is saved!")
    except IOError:
        print("error saving data :(")
    if pause:
        anykey()

def load(filename="save.sav"):
    clear()
    try:
        with open(filename, 'rb') as savefile:
            savedata = pickle.load(savefile)
        print("data loaded successfully.")
        anykey()
        return savedata
    except IOError:
        print("error loading data :C")
    anykey()

def quit(message="\nSee you!"):
    print(message)
    # restore terminal to the way it was 
    termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)
    raise SystemExit

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
        print("You have %d energy point left." % profile['energy'])
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
    for item in items:
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
        return 
    elif ch == 'l':
        global profile, items, queststatus
        profile, items, queststatus = load()

def commonOptions(ch):
    # hit 'p' or escape to pause
    if ch == 'p' or ch == '\x1B':
        pause()
        return True
    elif ch == 'h':
        helpme()
        return True
    return False

def helpme():
    clear()
    print('''Most actions in the game are performed by pressing A, B, C, or D
to perform actions that are described on screen. In some cases, the game may
ask for text input, after which you must press enter. At any time, you can
'pause' with ESC to see your inventory, stats, etc. or use backspace to undo
an action. Use S and L to save and load your progress, and Q to quit.
Use of this game while intoxicated may be illegal in some jurisdictions.''')
    anykey()

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

def fancyPrint(text, extraDelay):
    # prints lines character-by-character to be fancy
    # uses extraDelay to pause longer after bigger blocks of text
    # pass in -1 as extraDelay to force a standard pause
    # watch for ^C so it can quit prettily if needed
    #try:
    if True:
        text = replaceVariables(text)
        for character in text:
            sys.stdout.write(character)
            sys.stdout.flush()
            time.sleep(fancyPrintSpeed)
            if extraDelay > 0:
                # subtle difference between long lines and short ones
                extraDelay+=fancyPrintSpeed
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
    #except KeyboardInterrupt:
        #print()
        #quit()

class PreventBarfing:
    def __enter__(self):
        newtcattr = oldtcattr[:]
        newtcattr[3] = newtcattr[3] & ~termios.ECHO
        termios.tcsetattr(stdinfd, termios.TCSADRAIN, newtcattr)
    def __exit__(self, typ, value, callback):
        termios.tcsetattr(stdinfd, termios.TCSADRAIN, oldtcattr)


if __name__ == '__main__':
    savedata = load()
    profile = savedata[0]
    items = savedata[1]
    queststatus = savedata[2]
    print(replaceVariables("name is: %firstname%."))
    #save(savedata)
    #data = load()
    #print(data)
    while anykey("press any key to continue...") != 'q':
        pass
    helpme()
    stats(profile, items)
