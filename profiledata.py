# profiledata.py
# keeps track of the save profile

profile = {

        'firstname' : "Default",
        'lastname': "Namington",
        'gender' : "boy",
        'friendname' : "Ryan",
        'girlname' : "Katie",
        'weet' : 0,
        'posts' : 0,
        'money' : 0,
        'love' : 0,
        'flash' : 0,
        'sexy' : 0,

    # energy was defined separately, for some reason
    # <tass> because otherwise it would catch fire to the other variables
        'energy' : 15,

    # stats 
        'strongth' : 10,
        'dexterity' : 10,
        'charisma' : 10,
        'intellect' : 10,
        
        'soundWorks' : True,
}

items = {
        'a pack of ketchup' : True,
        'food' : False,
        'bolognasalad' : False,
        'pizza' : False,
        'ppizza' : False,
        'pppizza' : False,
        'tvskill' : False,
        'patience' : False,
        'rpatience' : False,
        'bike' : False,
        'mysql' : False,
        'showered' : False,
        'rab' : False,
        'oldlady' : False,
        'popcorn' : False,
        'nogun' : False,
        'gun' : False,
        'gunsold' : False,
        'girl' : False,
        'girls' : False,
        'boughtdrugs' : False,
        'nodrugs': False,
        'nnodrugs': False,
        'cheapdrugs': False,
        'donedrugs': False,
        'drugs': False,
        'macsdrugs': False,
        'playdrugs': False,
        'homedrugs': False,
        'outofdrugs': False,
        'outofdrugss': False,
        'cpu1': False,
        'cpu2': False,
        'cpu3': False,
        'ram1': False,
        'ram2': False,
        'ram3': False,
        'wifi': False,
        'wkam': False,
        'monitor': False,
        'cpu1i': False,
        'cpu2i': False,
        'cpu3i': False,
        'ram1i': False,
        'ram2i': False,
        'ram3i': False,
        'wifii': False,
        'wkami': False,
        'monitori': False,
        'powerweet': False,
        'picweet': False,
        'hobo': False,
        'slushskill': False,
        'wrench': False,
        'slushie': False
} 

queststatus = {
        'calledgirl' : False,
        'meetgirl' : False,
        'metgirl' : False,
        'hungout': False,
        'metdana': False,
        'dateplanned': False,
        'fixedtv' : False,
        'fixedslush': False,
        'bumbled' : False,
        'bolognaweet' : False,
        'robquest' : False,
        'robquestt' : False,
        'robthink' : False,
        'pizzaweet' : False,
        'shifty' : False,
        'shiftyy' : False,
        'doucheweet' : False,
        'patienceweet' : False,
        'slideweet' : False,
        'funweet' : False,
        'fmysql' : False,
        'shrine' : False,
}

savedata = (profile, items, queststatus)
