#!/usr/bin/python3
# main.py
# THIS DOES EVERYTHING!

from collections import deque
from sys import argv

from predicaments import Predicament
from funtoolkit import clear, playSound, anykey, quit, load
from settings import historycache
from savedata import profile, prefs

def main(start='title'):
    # i'm gonna make it automatically load here, and make the title screen
    # reflect that. ergo, you won't have to sit through nosound if you do
    # have your soundOff pref set to true
    # also, making a new save file probably won't overwrite your prefs
    load()
    # if playSound doesn't work, tell them the game will be mute
    if not playSound and not prefs['soundOff']:
        Predicament('nosound').play()
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
                anykey("No more history available.")
            continue
        # store this predicament on the list of previous predicaments 
        prevPredicaments.append(currentPredicament)
        currentPredicament = Predicament(nextPredicament)

if __name__ == '__main__':
    if len(argv) > 1:
        for predicament in argv[1:]:
            try:
                main(predicament)
            except KeyboardInterrupt:
                quit()
    else:
        try:
            main()
        except KeyboardInterrupt:
            quit()
