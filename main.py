#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

#import os
#from subprocess import call
from predicaments import predicaments
from funtoolkit import *
from profiledata import profile, items

# allows user to make a choice, returns their choice or false if they didn't
def play(predicament):
    clear()
    print(predicament['text'])
    letter = iter("abcdef")
    for option in predicament['choices']:
        print(next(letter), '-', option)
    choice = input("What do you want to do?\n").strip()
    if choice == 'stats':
        stats()
        return False
    elif choice == 'save':
        save( (profile, items) )
        return False
    elif choice == 'quit':
        raise SystemExit(0)
    elif choice not in predicament:
        return False
    else:
        return predicament[choice]

if __name__ == '__main__':
    currentPredicament = predicaments['title']
    while True:
        choice = False
        while not choice:
            choice = play(currentPredicament)
        try:
            currentPredicament = predicaments[choice]
        except KeyError:
            print("oops! predicament %s doesn't exist yet :C" % choice)
            raise SystemExit
