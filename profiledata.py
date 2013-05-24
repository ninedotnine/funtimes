# profiledata.py
# keeps track of the save profile

# these are important enough to be outside of the dict
# or are they?
# problem is: they're harder to pickle
#bran = "bran"
#rainey = "rainey"
#man = "boy"
#ryan = "ryan"
#katie = "katie"
#weet = 0
#posts = 0
#money = 0
#love = 0
#flash = 0
#sexy = 0
#energy = 15

profile = {

        'bran' : "bran",
        'rainey': "rainey",
        'man' : "boy",
        'ryan' : "ryan",
        'katie' : "katie",
        'weet' : 0,
        'posts' : 0,
        'money' : 0,
        'love' : 0,
        'flash' : 0,
        'sexy' : 0,

    # energy was defined separately, for some reason
        'energy' : 15,

    # stats 
        'strongth' : 10,
        'dexterity' : 10,
        'charisma' : 10,
        'intellect' : 10,
}

items = {
    # items
        'a pack of ketchup' : True,
        'shrine' : False,
        'food' : False,
        'bolognasalad' : False,
        'bolognaweet' : False,
        'pizza' : False,
        'ppizza' : False,
        'pppizza' : False,
        'pizzaweet' : False,
        'shifty' : False,
        'shiftyy' : False,
        'tvskill' : False,
        'patience' : False,
        'rpatience' : False,
        'bumbled' : False,
        'bike' : False,
        'mysql' : False,
        'fmysql' : False,
        'showered' : False,
        'rab' : False,
        'oldlady' : False,
        'doucheweet' : False,
        'patienceweet' : False,
        'slideweet' : False,
        'funweet' : False,
        'popcorn' : False,
        'robquest' : False,
        'robquestt' : False,
        'robthink' : False,
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
        'hungout': False,
        'metdana': False,
        'dateplanned': False,
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
        'fixedtv' : False,
        'fixedslush': False,
}

savedata = (profile, items, queststatus)
