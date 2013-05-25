# predicaments.py
# generates the dictionary that holds all the available predicaments

import os
 
# this is temporary. find a better way to do it.
# allow the user to set in-game, if possible...
preferredButtons = 'abcdef'
#preferredButtons = '123456'
#preferredButtons = 'aoeujk'

predicaments = {}

datadir = os.getcwd() + '/data/predicaments'

if not os.path.isdir(datadir):
    #os.makedirs(datadir)
    print("error: no data directory")
    raise SystemExit

for filename in os.listdir(datadir):
    basename, ext = os.path.splitext(filename)
    if ext != '.pred':
        print("WARNING: skipping %s/%s%s..." % (datadir, basename, ext))
        continue
    with open(datadir + '/' + filename, 'r') as fp:
        busy = False # keep track of whether we're currently reading a predicament
        tempdict = {} # create temp dict to store data while we parse it
        for line in fp:
            line = line.strip()
            if line == '': # skip blank lines
                continue 
            elif line.find("end of predicament") == 0:
                # at "end of predicament", copy tempdict to a sensible name and clear everything
                predicaments[tempdict['this']] = dict(tempdict)
                tempdict.clear()
                busy = False
                continue
            key, value = line.split('=')
            key = key.strip()
            if key == 'new predicament':
                # make sure we finished parsing the previous predicament
                if busy:
                    print("error reading predicaments.")
                    print("the problem is likely caused by " + tempdict['this'])
                    print("this is a fatal error. aborting")
                    raise SystemExit
                busy = True
                if tempdict:
                    # the tempdict should be empty at this point
                    tempdict.clear()
                tempdict['this'] = value.strip()
            elif key == 'text':
                # if there is no text yet, tell it that text will be a list
                if not 'text' in tempdict:
                    tempdict['text'] = []
                # add each line of text onto the prev line of text
                tempdict[key].append(value.strip())
            elif key == 'option':
                if not 'options' in tempdict:
                    tempdict['options'] = []
                if len(tempdict['options']) < 6: # we only allow abcdef - 6 options
                    tempdict['options'].append(value.strip())
            elif key == 'choice':
                if not 'choices' in tempdict:
                    tempdict['choices'] = []
                if len(tempdict['choices']) < 6:
                    tempdict['choices'].append(value.strip())
            else:
                tempdict[key] = value.strip()


if __name__ == '__main__':
    #print("content of", datadir, ": ", os.listdir(datadir))
    print()
    print("predicaments is")
    print(predicaments)
