# settings.py

# this is temporary. find a better way to do it.
# allow the user to set in-game, if possible...
preferredButtons = 'abcdef'
#preferredButtons = '123456'
#preferredButtons = 'aoeujk'

#fancyPrintSpeed = 0.015
fancyPrintSpeed = 0.001
#fancyPrintLineDelay = 0.500
fancyPrintLineDelay = 0.01

historycache = 10
defaultNonePrompt = '-->'
defaultNormalPrompt = 'What do you want to do?'
defaultInputPrompt = 'Please type something.'
defaultMultilinePrompt = 'Please type something. ^D when done.'


# figure this out later
#soundWorks = True
soundOn = False

# store terminal settings for restoration on quit()
import sys
import termios
from termios import tcflush, TCIOFLUSH
stdinfd = sys.stdin.fileno()
oldtcattr = termios.tcgetattr(stdinfd)
newtcattr = termios.tcgetattr(stdinfd)
