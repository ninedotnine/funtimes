# errors.py
# home of the big book of errors
# nothing else
# i know i said 80-character limit, but 1 error per line dammit

errors = (
    '',
    "what the hell? i can't find predicament %s\ndid you modify it while the game was running?",
    "wrong predicament found: %s",
    "what?? predicament %s doesn't exist, \nor didn't exist when the game was started! >:(",
    "in %s, %s was not ended correctly.",
    "reached the end of %s before finding %s\ndid you modify it while the game was running?",
    "in %s, %s has a type of '%s'.\ni don't know what the hell that means.",
    "didn't find an end of predicament for: %s",
    "no data directory",
    "%s has the type '%s', which is insane.",
    "if refers to '%s', which is not in profile.",
    "in %s, %s has %s after if.\nyou forgot to use a keyword, used an invalid keyword,\nor didn't include a condition after 'or' or 'and'.\nkeywords other than 'then' must precede an if.\nonly use 'then' after the final if condition.",
    "in %s, there is an unexpected 'end if' in predicament %s",
    "reached end of predicament %s before 'end if'.\nconditionals must remain within originating predicament.",
    "in %s, %s has a '%s' directive.\ni don't know what the hell that means.",
    "%s could not be found while searching for %s\ndid you rename or delete it while the game was running?",
    "in %s, %s has no type.",
    "reached end of %s while looking for 'end if'.\nthis is literally the end of the world.",
    "in %s, %s has no '=' on this line:\n%s\nmaybe you made a typo?",
    "%s refers to a '%s.wav'. there was an error accessing\nor playing this file. did you mistype the name?",
    "predicament %s tries to set %s to '%s'\nbut %s is supposed to be a number!",
    "predicament %s tries to set '%s' to a value\nbut that variable does not exist!",
    "predicament %s refers to %s.map,\nwhich doesn't exist in %s! >:(\nwhat kind of game are you playing at?",
)
