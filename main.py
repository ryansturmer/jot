import datetime, base64, pickle, os
from jinja2 import Environment, FileSystemLoader
from plugins import get_plugins
from notes import Note, TextNote, Notebook
from clock import ClockEvent
FILENAME = 'jotfile'
def setup_paths():
    import notes
    file = os.path.abspath(notes.__file__)
    while file and not os.path.isdir(file):
        file, ext = os.path.split(file)
    return file

if __name__ == "__main__":
    path = setup_paths()
    env = Environment(loader=FileSystemLoader(os.path.join(path, 'templates')))
    plugins = []
    for plugin in get_plugins(os.path.join(path, 'plugins')):
        print "Loaded plugin %s" % plugin.name
        plugins.append(plugin)

    try:
        notebook = Notebook.load(FILENAME)
        print "Loaded a notebook with %d notes" % len(notebook.notes)
    except Exception, e:
        print e
        import util
        title = util.ask("Enter notebook title:")
        notebook = Notebook(title)
        notebook.save(FILENAME)

    while True:
        try:
            has_plugin = False
            if notebook.timecard:
                t = notebook.total_time
                hours = int(t.total_seconds())/3600
                minutes = (int(t.total_seconds())-(3600*hours))/60
                seconds = int(t.total_seconds())-(3600*hours)-(60*minutes)
                prompt = "jot %02d:%02d:%02d >>" % (hours, minutes,seconds)
            else:
                prompt = "jot >>"

            cmd = raw_input(prompt).strip()
            note = None
            if cmd.startswith("!"):
                # Treat this as a command
                cmd = cmd.lstrip("!")
                try:
                    name = cmd.split()[0]
                except IndexError:
                    print "You must enter a command following the !"
                    continue
                for plugin in plugins:
                    if plugin.name == name:
                        has_plugin = True
                        note = plugin.command(cmd.lstrip(name))
                        break

                if not has_plugin:
                    print "No plugin loaded for '%s'" % cmd
                    continue
                if not note:
                    print "No note entered, user aborted."
                    continue


            elif cmd.startswith("?"):
                try:
                    cmd = cmd.lstrip("?").split()[0]
                except IndexError:
                    print ""
                    print "Type ?plugin to get help on specific commands"
                    print "Loaded plugins:"
                    for plugin in plugins:
                        print "   %s" % plugin.name
                    print ""
                    continue
                for plugin in plugins:
                    if plugin.name == cmd:
                        has_plugin = True
                        if plugin.__doc__:
                            print plugin.__doc__
                        else:
                            print "No help available for '%s'" % cmd
                        break
                
                if not has_plugin:
                    print "No plugin loaded for '%s'" % cmd

            else:
                note = TextNote(cmd)
            
            notebook.append(note)
            notebook.save(FILENAME)
            notebook.render('output.htm', env) 

        except KeyboardInterrupt:
            notebook.save(FILENAME)
            notebook.render('output.htm', env) 
            print "\nExiting"
            break

