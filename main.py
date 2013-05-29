#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

from collections import deque

from predicaments import Predicament
from funtoolkit import clear, playSound, initialize
from settings import historycache
from profiledata import profile

def main():
    initialize()
    # if playSound doesn't work, tell them the game will be mute
    profile['soundWorks'] = playSound('test')
    if profile['soundWorks']:
        currentPredicament = Predicament('title')
    else:
        currentPredicament = Predicament('nosound')
    # prevPredicaments is a queue. after each new predicament, append it.
    # it holds past Predicaments. it does not hold strings
    prevPredicaments = deque(maxlen=historycache)
    while True:
        nextPredicament = currentPredicament.play()
        if nextPredicament == currentPredicament.name:
            # if this is the same predicament, play it again
            continue
        elif nextPredicament == '\x7F':
            # go back to last predicament
            try:
                currentPredicament = prevPredicaments.pop()
            except IndexError:
                clear()
                anykey("no history available.")
            continue
        # store this predicament on the list of previous predicaments 
        prevPredicaments.append(currentPredicament)
        currentPredicament = Predicament(nextPredicament)

if __name__ == '__main__':
    main()
