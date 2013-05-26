#!/usr/bin/python3
# funtoolkit.py
# this is where common methods are declared.
# pause, clear, load, save, help, stats, etc. 

import os
import pickle
from subprocess import call
from profiledata import profile, items, queststatus

# define method to press any key. currently only works on unix
if os.name != 'nt':
    import sys, termios, tty
    # allows user to press any key to continue. thanks, Matthew Adams:
    # http://stackoverflow.com/questions/11876618/python-press-any-key-to-exit
    def anykey(message=''):
        # store stdin's file descriptor
        stdinFileDesc = sys.stdin.fileno() 
        # save stdin's tty attributes so I can reset it later
        oldStdinTtyAttr = termios.tcgetattr(stdinFileDesc) 
        if message:
            print(message)
        try:
            # set the input mode of stdin so that it gets added to 
            # char by char rather than line by line
            tty.setraw(stdinFileDesc)
            # read 1 byte from stdin (indicating that a key has been pressed)
            char = sys.stdin.read(1)
        finally:
            # reset 
            termios.tcsetattr(stdinFileDesc, termios.TCSADRAIN, oldStdinTtyAttr)
        if char == '\x03':
            raise KeyboardInterrupt
        if char == 'q':
            raise SystemExit
        return char

# define the method to clear the output, system-dependently
if os.name == 'nt':
    def clear():
        call('cls',shell=True)
else:
    def clear():
        call('clear',shell=True)

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

def stats(pause=True): 
    clear()
    print("CHARACTER STATS:")
    print("You are a %s named %s %s." % (profile['man'], profile['bran'],
                                        profile['rainey']))
    print("You currently have %d weet point(s)." % profile['weet'])
    print("You have $%d in your pocket." % profile['money'])
    print("You have %d energy point(s) left." % profile['energy'])
    if profile['strongth'] > 14:
        print("You are quite strong.")
    if profile['charisma'] > 14:
        print("You have a lot of charisma.")
    if profile['dexterity'] > 14:
        print("You are highly dextrous.")
    if profile['intellect'] > 14:
        print("You are very intelligent.")
    if profile['love'] == 2:
        print("You have a crush on %s" % profile['katie'])
    elif profile['love'] == 3:
        print("You're dating %s" % profile['katie'])
    elif profile['love'] == 4:
        print("You're in love with %s" % profile['katie'])
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
    print("\nMash 's' to save, 'l' to load, 'q' to quaff potion--er, I mean quit")
    ch = anykey()
    # hit 'p' or escape to unpause
    if ch == 'p' or ch == '\x1B':
        return
    elif commonOptions(ch):
        return
    elif ch == 'l':
        global profile, items, queststatus
        profile, items, queststatus = load()

def commonOptions(ch):
    # hit 'p' or escape to pause
    if ch == 'p' or ch == '\x1B':
        pause()
        return True
    elif ch == 's':
        save()
        return True
    elif ch == 'h':
        helpme()
        return True
    elif ch == 'q':
        raise SystemExit
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

# method what replaces variables' plaintext representations with the actual variable
def replaceVariables(text):
    # we only use dictionaries round these parts
    variables = {
        '~' : ' ',
        '%bran%' : profile['bran'],
        '%rainey%' : profile['rainey'],
    }
    for key, value in variables.items():
        text = text.replace(key, value)
    return text

if __name__ == '__main__':
    profile = savedata[0]
    items = savedata[1]
    queststatus = savedata[2]
    #save(savedata)
    data = load()
    #print(data)
    while anykey("press any key to continue...") != 'q':
        pass
    helpme()
    stats(profile, items)
