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
        if anykey() == 'p':
            pause()
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
        #choice = input("What do you want to do?\n").strip()
        print("\nWhat do you want to do?\n")
        #if 'inputtype' in predicament:
            #if predicament['inputtype'] == 'input':
                #return choice
        choice = anykey()
        while True:
            if choice == 'h':
                helpme()
                return False
            elif choice == 's':
                save()
                return False
            elif choice == 'q':
                print("oeuoaeuah")
                raise SystemExit(0)
            #elif choice not in predicament['choices']:
            elif choice not in letters:
                print("invalid option")
                choice = anykey()
            else:
                #return predicament[choice]
                return predicament['choices'][letters.index(choice)]

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
