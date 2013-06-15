# errors.py
# home of the big book of errors
# nothing else
# i know i said 80-character limit, but 1 error per line dammit

errors = (
    '',
    "what the hell? i can't find predicament %s\ndid you modify it while the game was running?", # 1
    "wrong predicament found: %s",
    "what?? predicament %s doesn't exist, \nor didn't exist when the game was started! >:(",
    "in %s, %s was not ended correctly.",
    "reached the end of %s before finding %s\ndid you modify it while the game was running?", # 5
    "in %s, %s has a type of '%s'.\ni don't know what the hell that means.",
    "%s doesn't have an end of predicament for %s",
    "no data directory",
    "%s has the type '%s', which is insane.",
    "in %s:\npredicament %s has the following line:\n%s\n'%s' is not a valid entry in %s.", # 10
    "in %s:\n%s has %s after if.\nyou forgot to use a keyword, used an invalid keyword,\nor didn't include a condition after 'or' or 'and'.\nkeywords other than 'then' must precede an if.\nonly use 'then' after the final if condition.",
    "in %s, there is an unexpected 'end if' in predicament %s",
    "reached end of predicament %s before 'end if'.\nconditionals must remain within originating predicament.",
    "in %s, %s has a '%s' directive.\ni don't know what the hell that means.",
    "%s could not be found while searching for %s\ndid you rename or delete it while the game was running?", # 15
    "in %s, %s has no type.",
    "reached end of %s while looking for 'end if'.\nthis is literally the end of the world.",
    "in %s, %s has no '=' on this line:\n%s\nmaybe you made a typo?",
    "%s refers to a '%s.wav'. there was an error accessing\nor playing this file. did you mistype the name?",
    "predicament %s tries to set %s to '%s'\nbut %s is supposed to be a number!", # 20
    "predicament %s tries to set %s['%s'] to a value\nbut that variable does not exist!",
    "predicament %s refers to %s.map,\nwhich doesn't exist in %s! >:(\nwhat kind of game are you playing at?",
    "a movement or action directive in predicament %s contains this line:\n %s\nwhich does not have a -> in it.\nmovement and action must declare the label, then ->,\nthen the name of the predicament which the labelled movement\nor action leads to. for example:\n Leave the house. -> outside",
    "in %s\npredicament %s has the following condition:\n%s\nbut %s is not of a comparable type\nif it was intended to contain a word, it will always contain a word\nsetting it to a number will not allow you to perform comparisons",
    "in %s\npredicament %s has the following condition:\n%s\nthis is trying to perform a comparison on %s,\nbut %s is neither a number nor a variable containing a number.\nyou are comparing apples and oranges, and i'm allergic.",
    # ^-- 25
    "in %s:\npredicament %s has this line:\n%s\nan if statement must contain 'is' or 'has'.",
    "in %s:\npredicament %s has this line:\n%s\nchecking the status of a quest can only be done\nby using 'done' or 'not done'.",
    "in %s:\npredicament %s has this line:\n%s\nit appears to refer to a dictionary called '%s'\nbut i don't know what that is... :/",
    "in %s:\npredicament %s has this line:\n%s\nnegating a comparison is pointless. just use the opposite.",
    "in %s, predicament %s has this line:\n%s\nit appears to refer to a dictionary called %s\nbut that's not a valid dictionary.", #30
    "in %s, predicament %s has this line:\n%s\nsetting must be done using 'to' or '='.",
    "in %s, predicament %s has this line:\n%s\n%s is not sensible.\nquest entries must be set to 'done' or 'not done'.",
    "in %s, predicament %s\ntries to %s %s from player.\nthis item does not exist.",
)
