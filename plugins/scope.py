from notes import Note
from plugins import Plugin
from util import ask
import os, base64
import agilent

SCOPE_SERIAL_PORT = "/dev/ttyUSB0"
class ScopeScreenshotNote(Note):
    def __init__(self, summary, scope_data):
        Note.__init__(self)
        self.title = "Scope Screenshot"
        self.summary = summary
        self.image_data = "data:image/png;base64,%s" % (base64.b64encode(scope_data))
    def render(self):
        return '<img src="%s"/>' % self.image_data

class ScopePlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "scope")
    
    def command(self, cmd_string):
        scope = agilent.Scope(SCOPE_SERIAL_PORT)
        png_data = scope.get_screenshot(agilent.Scope.PNG)
        return ScopeScreenshotNote(cmd_string, png_data)

