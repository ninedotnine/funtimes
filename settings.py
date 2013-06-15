# settings.py
import os

datadir = os.getcwd() + '/data/'
if not os.path.isdir(datadir):
    print("\ncould not find data directory\n")
    raise KeyboardInterrupt

# this is temporary. find a better way to do it.
# allow the user to set in-game, if possible...
#actionButtons = 'abcdef'
actionButtons = '123456'
#actionButtons = 'aoeujk'
movementButtons = 'wsad' # up, down, left, right
#movementButtons = 'jkhl' # up, down, left, right

#fancyPrintSpeed = 0.015
fancyPrintSpeed = 0.001
#fancyPrintLineDelay = 0.500
fancyPrintLineDelay = 0.01

historycache = 10
defaultNonePrompt = '-->'
defaultNormalPrompt = 'What do you want to do?'
defaultInputPrompt = 'Please type something.'
defaultMultilinePrompt = 'Please type something. ^D when done.'

# use unicode arrows if the character set supports it
try:
    arrows = '\u2191\u2193\u2190\u2192'
    print(arrows, file=open(os.devnull,'w'))
except UnicodeEncodeError:
    arrows = '^v<>'

lineLength = 69

soundOn = False
clearOn = True

if __name__ == '__main__':
    for thing in dir():
        if not thing.startswith('__'):
            print(thing, '=', eval(thing))
