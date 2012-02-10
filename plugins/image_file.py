from notes import Note
from plugins import Plugin
from util import ask
import os, base64

class ImageFileNote(Note):
    def __init__(self, summary, filename):
        Note.__init__(self)
        self.title = "Image"
        self.summary = summary
        path, ext = os.path.splitext(filename)
        with open(filename, 'rb') as fp:
            data = fp.read()
        self.image_data = "data:image/%s;base64,%s" % (ext, base64.b64encode(data))
    def render(self):
        return '<img src="%s"/>' % self.image_data

class ImageFilePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "image")
    
    def command(self, cmd_string):
        summary = ask('Enter image description:')
        filename = os.path.abspath(cmd_string.strip())
        return ImageFileNote(summary, filename)

