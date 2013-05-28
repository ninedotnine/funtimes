#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

from predicaments import predicaments, Predicament
from funtoolkit import *
from settings import *
from collections import deque

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
    for line in predicament.text:
        if "fancytext" in predicament.disable:
            print(replaceVariables(line))
        else:
            fancyPrint(line)
    # decide what the prompt will be
    if predicament.prompt:
        # if there is a custom prompt, just use it
        prompt = "\n[" + predicament.prompt + "]"
    elif predicament.disable and "prompt" in predicament.disable:
        # otherwise, disable the prompt if it's disabled
        prompt = ""
    elif not predicament.disable or "prompt" not in predicament.disable:
        # or, just use the default prompt depending on inputtype
        if predicament.inputtype == 'none':
            prompt = "\n[" + defaultNonePrompt + "]"
        elif predicament.inputtype == 'normal':
            prompt = "\n[" + defaultNormalPrompt + "]"
        elif predicament.inputtype == 'input':
            prompt = "\n[" + defaultInputPrompt + "]"
    # once we're done fancyprinting, we don't want to redraw the predicament if
    # we return to it while it's in memory (unpausing, using backspace, etc)
    if "fancytext" not in predicament.disable \
    and "normal" not in predicament.inputtype:
        # normal predicaments still have some fancyprinting to do
        predicament.disable.append("fancytext")
    if predicament.inputtype == 'none':
        ch = anykey(prompt)
        if commonOptions(ch):
            return predicament.name
        # hit backspace or ^H to go back
        elif ch == '\x08' or ch == '\x7F':
            return '\x7F'
        # hit ^R to forcibly redraw the text
        elif ch == '\x12':
            predicament.disable.remove("fancytext")
            return predicament.name
        return predicament.goto
    elif predicament.inputtype == 'input':
        print(prompt)
        # because invalid input would be a newline, we don't want the newline
        # again after the first one. this'll keep it looking consistent.
        prompt = prompt[1:]
        try:
            profile[predicament.result] = input().strip()
            while profile[predicament.result] == '':
                # output the last line of text until a valid input is provided
                profile[predicament.result] = input(prompt + "\n").strip()
        except KeyboardInterrupt:
            quit()
        return predicament.goto
    elif predicament.inputtype == 'normal':
        letters = preferredButtons[:len(predicament.options)]
        iterletters = iter(letters)
        #print("options", len(predicament['options']))
        print()
        for option in predicament.options:
            string = next(iterletters) + ' - ' + option
            if 'fancytext' in predicament.disable:
                print(string)
            else:
                # *now* normal predicaments are done fancyprinting
                predicament.disable.append("fancytext")
                fancyPrint(string)
        choice = anykey(prompt)
        while True:
            if commonOptions(choice):            
                return predicament.name
            # hit backspace or ^H to go back
            elif choice == '\x08' or choice == '\x7F':
                return '\x7F'
            # hit ^R to forcibly redraw the text
            elif choice == '\x12':
                predicament.disable.remove("fancytext")
                return predicament.name
            elif choice not in letters:
                choice = anykey(prompt)
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
