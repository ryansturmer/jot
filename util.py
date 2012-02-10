class NoEntry(Exception): pass

def ask(question, default="", persist=False, coerce=lambda x : x):
    while True:
        try:
            s = raw_input(question + " ")
            if s:
                try:
                    s = coerce(s)
                    return s
                except Exception, e:
                    print e
                    continue
            else:
                if not persist:
                    return default
                else:
                    continue
        except KeyboardInterrupt:
            raise NoEntry
    
def ask_yesno(question, default=None, persist=False):
    def yn(x):
        x = x.strip().lower()
        if x in 'yn':
            return True if x == 'y' else False
        else:
            raise Exception("Please enter y or n")
    ask(question, default, persist, coerce=yn)

