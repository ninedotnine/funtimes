class Predicament:
    """this is a class for holding a predicament!"""

    # class variable, accessible anywhere, shared by instances of Predicament
    numPredicaments = 0
    
    #def __init__(self, name, inputtype, text):
        # name, inputtype are strings, text is a list
    def __init__(self, tempdict):
        # to make things easier, for now we'll just pass in the tempdict
        Predicament.numPredicaments += 1
        self.name = tempdict['this']
        self.inputtype = tempdict['inputtype']
        self.text = tempdict['text']

        self.setvars = None
        if 'set' in tempdict:
            self.setvars = tempdict['set']

        if self.inputtype == 'normal':
            self.options = tempdict['options']
            self.choices = tempdict['choices']
        elif self.inputtype == 'none':
            self.next = tempdict['next']
        elif self.inputtype == 'input':
            self.next = tempdict['next']
            self.result = tempdict['result']
        else:
            print("unknown input type:" + self.inputtype)
            raise SystemExit

    def __str__(self):
        return 'Predicament: %s: %s' % (self.name, self.text)

if __name__ == '__main__':
    d = {'this':'gay', 'inputtype':'none', 'text':["this pred sucks!"], 'next':'oops'}
    print(Predicament(d))
    print(dir(d))
