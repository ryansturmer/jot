from notes import Note
from plugins import Plugin
from util import ask
import subprocess

class ExecNote(Note):
    def __init__(self, cmd, summary, stdout, stderr):
        Note.__init__(self)
        self.stdout = stdout
        self.stderr = stderr
        self.title = cmd
        self.summary = summary

    def render(self):
        scrubbed = self.stdout.replace(' ','&nbsp;').replace('\n','<br />')
        return '''<div class="noteMono">%s</div>''' % scrubbed

class ExecPlugin(Plugin):
    def __init__(self):
        Plugin.__init__(self, "exec")
    
    def command(self, cmd_string):
        proc = subprocess.Popen(cmd_string, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout,stderr = proc.communicate()
        print ""
	print stdout
	print ""
	summary = ask("Enter a comment for this output")
        return ExecNote(cmd_string, summary, stdout, stderr)
