#!/usr/bin/python3
# funtoolkit.py
# this is where common methods are declared.
# clear, load, save, help, stats, etc. 

import os
import pickle
from subprocess import call

# define the method to clear the output, system-dependently
if os.name == 'nt':
    def clear():
        call('cls',shell=True)
else:
    def clear():
        call('clear',shell=True)

def save(savedata, filename="save.sav"):
    clear()
    try: 
        with open(filename, 'wb') as savefile: 
            pickle.dump(savedata, savefile)
        print("your data is saved!")
    except IOError:
        print("error saving data :(")
    input()

def load(filename="save.sav"):
    clear()
    try:
        with open(filename, 'rb') as savefile:
            savedata = pickle.load(savefile)
            print("data loaded successfully.")
            return savedata
    except IOError:
        print("error loading data :C")
    input()

def stats(profile, items):
    clear()
    print("CHARACTER STATS:")
    print("you are a %s name %s %s." % (profile['man'], profile['bran'],
                                        profile['rainey']))
    print("you currently have %d weet point(s)." % profile['weet'])
    print("you have $%d in your pocket" % profile['money'])
    print("you have %d energy point(s) left." % profile['energy'])
    if profile['strongth'] > 14:
        print("you are quite strong.")
    if profile['charisma'] > 14:
        print("you have a lot of charisma.")
    if profile['dexterity'] > 14:
        print("you are highly dextrous.")
    if profile['intellect'] > 14:
        print("you are very intelligent.")
    if profile['love'] == 2:
        print("you have a crush on %s" % katie)
    elif profile['love'] == 3:
        print("you're dating %s" % katie)
    elif profile['love'] == 4:
        print("you're in love with %s" % katie)
    print("ITEMS ON HAND:")
    for item in items:
        if items[item] == True:
            print(item)
    input()

def helpme():
    clear()
    print('Most actions are performed by typing A, B, C, or D, then hitting \
the enter or return key on your keyboard. Some portions of the game may \
require different commands, as dictated by the instructions that appear \
in-game. At any point, you can type "stats" to view your character stats and \
inventory, or type "save" to save the game, or type "help" to see... this.')
    print("YOU MUST SAVE THE GAME IF YOU WANT TO KEEP YOUR PROGRESS.")
    input()

if __name__ == '__main__':
    from profiledata import *
    profile = savedata[0]
    items = savedata[1]
    queststatus = savedata[2]
    save(savedata)
    data = load()
    #print(data)
    input()
    help()
    stats(profile, items)
