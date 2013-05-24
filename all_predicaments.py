# all_predicaments.py
# definitions for predicaments go here

title = {
        'text' : """\
####### #     # #     # ####### ### #     # #######  #####
#       #     # ##    #    #     #  ##   ## #       #     #
#       #     # # #   #    #     #  # # # # #       # 
#####   #     # #  #  #    #     #  #  #  # #####    #####
#       #     # #   # #    #     #  #     # #             #
#       #     # #    ##    #     #  #     # #       #     #
#        #####  #     #    #    ### #     # #######  #####
                   (hope you have fun!)

        """,
        'choices' : [
            "Start a new game.",
            "Continue your old game.",
            "Read the help file."
        ],
        'a' : "makeNewSaveFile",
        'b' : "continueSaveFile",
        'c' : "helpme"
}

helpme = {
        'text' : """\
Most actions are performed by typing A, B, C, or D, then hitting the enter
or return key on your keyboard. Some portions of the game may require different
commands, as dictated by the instructions that appear in-game. At any point,
you can type "stats" to view your character stats and inventory, or type "save"
to save the game. YOU MUST SAVE THE GAME IF YOU WANT TO KEEP YOUR PROGRESS.
        """,
        'choices' : title['choices'],
        'a' : title['a'], 
        'b' : title['b'], 
        'c' : title['c']
}
