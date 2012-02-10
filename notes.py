from clock import ClockEvent, compute_time
import pickle, datetime, os
import getpass

def FORMAT_DATE(d):
    return d.strftime("%Y-%m-%d %H:%M:%S")

class Note(object):
    def __init__(self):
        self.datestamp = datetime.datetime.now()
        self.title = ""

    def render(self):
        return None
   
    @property
    def body(self):
        return self.render()

    @property
    def date_string(self):
        return FORMAT_DATE(self.datestamp)

class TextNote(Note):
    def __init__(self, text):
        Note.__init__(self)
        self.summary = text

class Notebook(object):
    def __init__(self, title="Title"):
        self.notes = []
        self.timecard = []
        self.title = title
        self.created = datetime.datetime.now()
        self.modified = self.created
        self.user = getpass.getuser()

    @property
    def created_string(self):
        return FORMAT_DATE(self.created)

    @property
    def modified_string(self):
        return FORMAT_DATE(self.modified)

    def __iter__(self):
        return iter(enumerate(self.notes))

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as fp:
            obj = pickle.load(fp)
        return obj

    def save(self, filename):
        self.modified = datetime.datetime.now()
        with open(filename, 'wb') as fp:
            pickle.dump(self, fp)
        
    def append(self, note):
        if isinstance(note, Note):
            self.notes.append(note)
        elif isinstance(note, ClockEvent):
            self.timecard.append(note)

    @property
    def total_time(self):
        return compute_time(self.timecard)

    def render(self, filename, env):
        import main
        template = env.get_template('template.htm')
        s = template.render(notes=self)
        with open(filename, 'w') as fp:
            fp.write(s)


