# savedata.py
# keeps track of the save profile

from settings import datadir

def populateDictionary(dictionary):
    try:
        with open(datadir + dictionary + '.dat', 'r') as fp:
            dictionary = {}
            for line in fp:
                dictionary[line.strip()] = False
    except FileNotFoundError:
        print("\ncould not find '" + dictionary + "' in data directory\n")
        raise SystemExit # should be safe since this runs before anything else
    return dictionary

profile = {

        'firstname' : "Default",
        'lastname': "Namington",
        'gender' : "boy",
        'friendname' : "Ron",
        'girlname' : "Katie",
        'weet' : 0,
        'posts' : 0,
        'money' : 0,
        'love' : 0,
        'flash' : 0,
        'sexy' : 0,
        'energy' : 15,
        
    # general-purpose garbage variable
        'progress' : 0,

    # stats 
        'strongth' : 10,
        'dexterity' : 10,
        'charisma' : 10,
        'intellect' : 10,
        
        'latestPredmap' : None,
        'latestMapname' : None,
}

items = populateDictionary('items')

quests = populateDictionary('quests')

savedata = (profile, items, quests)
