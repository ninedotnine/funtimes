#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

from predicaments import predicaments, Predicament
from funtoolkit import *
from collections import deque
from settings import preferredButtons, historycache

# moved this to funtoolkit
# from profiledata import profile, items, queststatus

# allows user to make a choice, returns their choice or false if they didn't
# i think i took out all the possible false returns...
# the predicament parameter is one of the dictionaries stored in predicaments 
# the predicament parameter is a Predicament 
# should return a string
def play(predicament):
    global profile, items, queststatus
    clear()
    #predicament = Predicament(predicament)
    #if there are SET statements in predicament, do those before printing text
    if predicament.setvars:
        for statement in predicament.setvars:
            # make tuple readable
            variable, value = statement[0], statement[1]
            try:
                profile[variable] = value
            #if variable not in profile.keys():
            except KeyError:
                print("error: probable invalid SET statement in predicament",
                       predicament.name)
                print("refers to nonexistent variable '%s'" % variable)
                print("this is a fatal error. aborting")
                raise SystemExit
            #profile[variable] = value
    for line in predicament.text:
        print(replaceVariables(line))
    if not predicament.inputtype:
        print("error: predicament %s has no inputtype" % predicament.name)
        raise SystemExit
    elif predicament.inputtype == 'none':
        ch = anykey()
        if commonOptions(ch):
            return predicament.name
        # hit backspace or ^H to go back
        elif ch == '\x08' or ch == '\x7F':
            return '\x7F'
        return predicament.goto
    elif predicament.inputtype == 'input':
        try:
            profile[predicament.result] = input().strip()
            while profile[predicament.result] == '':
                # output the last line of text until a valid input is provided
                profile[predicament.result] = input(predicament.text[-1] + '\n').strip()
        except KeyboardInterrupt:
            quit()
        return predicament.goto
    elif predicament.inputtype == 'normal':
        letters = preferredButtons[:len(predicament.options)]
        iterletters = iter(letters)
        #print("options", len(predicament['options']))
        print()
        for option in predicament.options:
            print(next(iterletters), '-', option)
        choice = anykey("\nWhat do you want to do?")
        while True:
            if commonOptions(choice):
                return predicament.name
            elif choice == '\x08' or choice == '\x7F':
                return '\x7F'
            elif choice not in letters:
                choice = anykey("invalid option")
            else:
                return predicament.goto[letters.index(choice)]


if __name__ == '__main__':
    currentPredicament = Predicament('title')
    # prevPredicaments is a queue. after each new predicament, append it.
    # it holds past Predicaments. it does not hold strings
    prevPredicaments = deque(maxlen=historycache)
    while True:
        nextPredicament = play(currentPredicament)
        if nextPredicament == '\x7F':
            # go back to last predicament
            try: 
                currentPredicament = prevPredicaments.pop()
            except IndexError:
                clear()
                anykey("no history available.")
            continue
        nextPredicament = Predicament(nextPredicament)
        if nextPredicament.name != currentPredicament.name:
            prevPredicaments.append(currentPredicament)
            currentPredicament = nextPredicament
        #if currentPredicament not in predicaments:
            #print("oops! predicament '%s' doesn't exist yet :C" % nextPredicament)
            #raise SystemExit
