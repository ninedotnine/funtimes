# all_predicaments.py
# definitions for predicaments go here

title = {
        'inputtype' : None,
        'text' : """\
####### #     # #     # ####### ### #     # #######  #####
#       #     # ##    #    #     #  ##   ## #       #     #
#       #     # # #   #    #     #  # # # # #       # 
#####   #     # #  #  #    #     #  #  #  # #####    #####
#       #     # #   # #    #     #  #     # #             #
#       #     # #    ##    #     #  #     # #       #     #
#        #####  #     #    #    ### #     # #######  #####
                   (hope you have fun!)

commands: save load stats help quit
press enter to start!
        """,
        # 'choices' : [
        # "Start a new game.",
        # "Continue your old game.",
        # "Read the help file."
        # ],
        #'a' : "makeNewSaveFile",
        #'b' : "continueSaveFile",
        #'c' : "helpme"
        'next' : createCharacter,
}

helpme = {
        'inputtype' : 'normal',
        'text' : """\
Most actions are performed by typing A, B, C, or D, then hitting the enter
or return key on your keyboard. Some portions of the game may require different
commands, as dictated by the instructions that appear in-game. At any point,
you can type "stats" to view your character stats and inventory, or type "save"
to save the game. YOU MUST SAVE THE GAME IF YOU WANT TO KEEP YOUR PROGRESS.
        """,
        #'choices' : title['choices'],
        #'a' : title['a'], 
        #'b' : title['b'], 
        #'c' : title['c']
}

createCharacter = {
        'inputtype' : None,
        'text' : """
Your best friend sits across from you at Pizza Pizza, picking
at his teeth idly. He glances up at the spotty clerk behind the
counter.""",
        'next' : createCharacter2,
}

createCharacter2 = {
        'inputtype' : None,
        'text' : """
"Alright," he says. "You gonna go order, or should I?"
This is the third time he's asked you this.
Making sure to roll your eyes as visibly as possible, you stand
up from your table and walk up to the counter.""",
        'next' : createCharacter3,
}

createCharacter3 = {
        'inputtype' : 'input',
        'text' : """
"Medium pepperoni." The spotty clerk takes your money.
"Name?"
"What do you need that for?"
"We don't do numbers anymore," he says dully. "I'll call you up to
the counter when your pizza is ready." 
        What is your name?""",
        'next' : createCharacter4,
}

createCharacter4 = { 
        'inputtype' : 'input',
        'text' : """
NAME HERE.
The spotty clerk just rolls his eyes.
"LAST name?"
        What is your LAST name?""",
        'next' : createCharacter5,

}

createCharacter5 = {
        'inputtype' : None,
        'text' : """
LASTNAME HERE.
"Thank you," he says. He turns over his shoulder and yells to someone
in the back, "%bran% %rainey% is in dire need of a pepperoni!
Thick and juicy if possible! Thank you."
He turns back and winks at you.""",
        'next' : createCharacter6,
}

createCharacter6 = {
        'inputtype' : 'normal',
        'text' : """
The spotty clerk's sudden advance turns your stomach. Before heading
back to your table, you make a detour to the washrooms.
""",
        'choices' : [
            "Go into the women's room.",
            "Go into the men's room."
        ],
        'a' : 'mans',
        'b' : 'womans',
}


        
