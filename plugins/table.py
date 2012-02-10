from notes import Note
from plugins import Plugin
from util import ask, NoEntry
import os, base64
from jinja2 import Template

class TableNote(Note):
    def __init__(self, summary, data, header=False):
        Note.__init__(self)
        self.title = "Table"
        self.summary = summary
        self.header = header
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

class TablePlugin(Plugin):
    '''
    TablePlugin

    Command format: !table <no arguments>

    Enter a table summary, followed by any number of comma separated lists of strings.
    The entered data will be formatted into an HTML table.
    '''
    def __init__(self):
        Plugin.__init__(self, "table")
    
    def command(self, cmd_string):
        tokens = cmd_string.lower().strip().split()
        summary = ask("Table summary: ")
        table = []
        while True:
            try:
                s = ask("Enter row of data (comma separated)", persist=False)
                if not s:
                    break
                row = s.split(",")
                table.append(row)
            except NoEntry:
                return None;

        return TableNote(summary, table, header="header" in tokens)
