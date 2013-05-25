#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

from predicaments import predicaments, preferredButtons
from funtoolkit import *

# moved this to funtoolkit
# from profiledata import profile, items, queststatus

# allows user to make a choice, returns their choice or false if they didn't
# should return a string
def play(predicament):
    global profile, items, queststatus
    clear()
    print(predicament)
    for line in predicament['text']:
        print(line)
    if 'inputtype' not in predicament:
        print("error: predicament %s has no inputtype" % predicament)
        raise SystemExit
    elif predicament['inputtype'] == 'none':
        ch = anykey()
        if commonOptions(ch):
            return predicament['this']
        # maybe backspace to go back?
        elif ch == 'b':
            return predicament['prev']
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
    #currentPredicament = predicaments['title']
    currentPredicament = 'title'
    # start with prevPredicament assigned to title as well because "what else"
    prevPredicament = predicaments[currentPredicament]['this']
    while True:
        predicaments[currentPredicament]['prev'] = prevPredicament 
        nextPredicament = play(predicaments[currentPredicament])
        prevPredicament = predicaments[currentPredicament]['this']
        currentPredicament = nextPredicament
        if currentPredicament not in predicaments:
            print("oops! predicament '%s' doesn't exist yet :C" % nextPredicament)
            raise SystemExit
        #try:
            #currentPredicament = predicaments[nextPredicament]
        #except KeyError:
            #print("oops! predicament '%s' doesn't exist yet :C" % nextPredicament)
            #raise SystemExit
