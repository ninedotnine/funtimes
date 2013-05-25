#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

from predicaments import predicaments, preferredButtons
from funtoolkit import *

# moved this to funtoolkit
# from profiledata import profile, items, queststatus

# allows user to make a choice, returns their choice or false if they didn't
# the predicament parameter is one of the dictionaries stored in predicaments 
# should return a string
def play(predicament):
    global profile, items, queststatus
    clear()
    #print(predicament)
    for line in predicament['text']:
        print(replaceVariables(line))
    if 'inputtype' not in predicament:
        print("error: predicament %s has no inputtype" % predicament)
        raise SystemExit
    elif predicament['inputtype'] == 'none':
        ch = anykey()
        if commonOptions(ch):
            return predicament['this']
        # hit backspace or ^H to go back
        elif ch == '\x08' or ch == '\x7F':
            #return predicament['prev']
            return '\x7F'
        return predicament['next']
    elif predicament['inputtype'] == 'input':
        profile[predicament['result']] = input().strip()
        while profile[predicament['result']] == '':
            # output the last line of text until a valid input is provided
            profile[predicament['result']] = input(predicament['text'][-1] + '\n').strip()
        return predicament['next']
    elif predicament['inputtype'] == 'normal':
        letters = preferredButtons[:len(predicament['options'])]
        iterletters = iter(letters)
        #print("options", len(predicament['options']))
        print()
        for option in predicament['options']:
            print(next(iterletters), '-', option)
        choice = anykey("\nWhat do you want to do?")
        while True:
            if commonOptions(choice):
                return predicament['this']
            elif choice not in letters:
                choice = anykey("invalid option")
            else:
                return predicament['choices'][letters.index(choice)]


if __name__ == '__main__':
    currentPredicament = 'title'
    # prevPredicaments is a list. after each new predicament, append it.
    prevPredicaments = ['title']
    while True:
        try:
            nextPredicament = play(predicaments[currentPredicament])
        except KeyError:
            print("oops! predicament '%s' doesn't exist yet :C" 
                  % nextPredicament)
            raise SystemExit
        if nextPredicament == '\x7F':
            # go back to last predicament
            try: 
                currentPredicament = prevPredicaments.pop()
            except IndexError:
                anykey("no history available.")
            continue
        elif nextPredicament != currentPredicament:
            prevPredicaments.append(currentPredicament)
            currentPredicament = nextPredicament
        #if currentPredicament not in predicaments:
            #print("oops! predicament '%s' doesn't exist yet :C" % nextPredicament)
            #raise SystemExit
