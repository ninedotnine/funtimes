#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

from predicaments import predicaments, preferredButtons
from funtoolkit import *

# moved this to funtoolkit
# from profiledata import profile, items, queststatus

# allows user to make a choice, returns their choice or false if they didn't
def play(predicament):
    global profile, items, queststatus
    clear()
    for line in predicament['text']:
        print(line)
    if 'inputtype' not in predicament:
        print("error: predicament %s has no inputtype" % predicament)
        raise SystemExit
    elif predicament['inputtype'] == 'none':
        if commonOptions(anykey()):
            return predicament['this']
        return predicament['next']
    elif predicament['inputtype'] == 'input':
        profile[predicament['result']] = input().strip()
        while profile[predicament['result']] == '':
            profile[predicament['result']] = input(predicament['text'][-1] + '\n').strip()
        return predicament['next']
    elif predicament['inputtype'] == 'normal':
        letters = preferredButtons[:len(predicament['options'])]
        letteriter = iter(letters)
        print("options", len(predicament['options']))
        for option in predicament['options']:
            print(next(letteriter), '-', option)
        choice = anykey("\nWhat do you want to do?\n")
        while True:
            if commonOptions(choice):
                return predicament['this']
            elif choice not in letters:
                choice = anykey("invalid option")
            else:
                return predicament['choices'][letters.index(choice)]

if __name__ == '__main__':
    currentPredicament = predicaments['title']
    while True:
        nextPredicament = play(currentPredicament)
        try:
            currentPredicament = predicaments[nextPredicament]
        except KeyError:
            print("oops! predicament '%s' doesn't exist yet :C" % choice)
            raise SystemExit
