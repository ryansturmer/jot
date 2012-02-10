from notes import Note
from plugins import Plugin
from util import ask, NoEntry
import os, base64
from jinja2 import Template
import mycsv

class CSVNote(Note):
    def __init__(self, summary, data):
        Note.__init__(self)
        self.title = "Table"
        self.summary = summary
        self.data = data

    def render(self):
        s = r'''
        <table class="noteDataTable">
            {% for row in table %}
            <tr>
                {% for cell in row %}
                <td class="noteDataTable">{{cell}}</td>
                {% endfor %}
            </tr>
            {% endfor %}
        </table>
        '''
        template = Template(s)
        return template.render(table=self.data)

class CSVPlugin(Plugin):
    '''
    CSVPlugin

    Command format: !csv <filename>

    Store the provided file in the notes as a data table.

    '''
    def __init__(self):
        Plugin.__init__(self, "csv")
    
    def command(self, cmd_string):
        filename = cmd_string.strip()
        with mycsv.CSVFile(filename) as fp:
            data = fp.readlines()
        print "Loaded %d lines from %s" % (len(data), filename)
        summary = ask("Table summary: ")
        
        return CSVNote(summary, data)

