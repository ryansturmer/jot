from notes import Note
from plugins import Plugin
from util import ask, NoEntry
import os, base64
from jinja2 import Template

class LinkNote(Note):
    def __init__(self, link, name=None, body=None):
        Note.__init__(self)
        self.title = "Link"
        self.link = link
        self.name = name or link
        self.summary_body = body
    @property
    def summary(self):
        return '<a href="%s">%s</a>' % (self.link, self.name)

    def render(self):
        return self.summary_body

class LinkPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "link")
    
    def command(self, cmd_string):
        try:
            link = ask("Link URL: ")
            name = ask("Link Text (You may leave blank): ").strip() or None
            body = ask("Additional description of the link? ") or None
        except NoEntry:
            return None

        return LinkNote(link, name, body)

