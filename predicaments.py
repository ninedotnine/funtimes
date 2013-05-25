# predicaments.py
# generates the dictionary that holds all the available predicaments

import os
import json
 
# this is temporary. find a better way to do it.
# allow the user to set in-game, if possible...
preferredButtons = 'abcdef'
#preferredButtons = '123456'
#preferredButtons = 'aoeujk'

predicaments = {}

datadir = 'data/predicaments'

if not os.path.isdir(datadir):
    os.makedirs(datadir)

for filename in os.listdir(datadir):
    basename, ext = os.path.splitext(filename)
    if ext != '.pred':
        print("WARNING: skipping %s/%s%s..." % (datadir, basename, ext))
        continue
    with open(datadir + '/' + filename, 'r') as fp:
        busy = False # keep track of whether we're currently reading a predicament
        tempdict = {}
        for line in fp:
            line = line.strip()
            if line == '': # skip blank lines
                continue 
            elif line.find("end of predicament") == 0:
                predicaments[tempdict['this']] = dict(tempdict)
                tempdict.clear()
                busy = False
                continue
            key, value = line.split('=')
            key = key.strip()
            if key == 'new predicament':
                # just to make sure...
                if busy:
                    print("error reading predicaments. aborting")
                    raise SystemExit
                busy = True
                if tempdict:
                    # the tempdict should be empty at this point
                    tempdict.clear()
                tempdict['this'] = value.strip()
            elif key == 'text':
                # the text will be a list 
                if not 'text' in tempdict:
                    tempdict['text'] = []
                tempdict[key].append(value.strip())
            elif key == 'option':
                if not 'options' in tempdict:
                    tempdict['options'] = []
                tempdict['options'].append(value.strip())
            elif key == 'choice':
                if not 'choices' in tempdict:
                    tempdict['choices'] = []
                tempdict['choices'].append(value.strip())
            else:
                tempdict[key] = value.strip()


if __name__ == '__main__':
    #print("content of", datadir, ": ", os.listdir(datadir))
    print()
    print("predicaments is")
    print(predicaments)
