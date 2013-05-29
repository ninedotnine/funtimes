#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

from collections import deque

from predicaments import Predicament
from settings import historycache

def main(start='title'):
    currentPredicament = Predicament(start)
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
