import os,sys,traceback
import inspect
import dummy

class Plugin(object):
    def __init__(self, name):
        self.name = name

    def command(self, command):
        raise NotImplemented

    def __contains__(self, command):
        return command in self.commands

# Stuff below is for loading plugins
def add_sys_path(new_path):
    new_path = os.path.abspath(new_path)
    do = -1
    if os.path.exists(new_path):
        do = 1
        y = new_path
        if sys.platform == 'win32':
            y = new_path.lower()
        for x in sys.path:
            x = os.path.abspath(x)
            if sys.platform == 'win32':
                x = x.lower()
            if y in (x, x + os.sep):
                do = 0
                break
        if do:
            sys.path.insert(0, new_path)
    return do

def remove_sys_path(path):
    path = os.path.abspath(path)
    return sys.path.remove(path)

def import_module(name):
    name = name.strip(".")
    mod = __import__(name)
    reload(mod)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod
    
def get_modules(folder):
    modules = []
    folder = os.path.abspath(folder)
    if os.path.exists(folder):
        modified_path = add_sys_path(folder)
        for path, dirs, files in os.walk(folder):
            path = path.replace(folder, '')
            path = path.replace(os.sep, '.')
            path = path.strip('.')
            prefix = path + '.'
            py_files = [prefix+file[:-3] for file in files if file.endswith('.py')]
            pyc_files = [prefix+file[:-4] for file in files if file.endswith('.pyc')]
            module_names = set(py_files + pyc_files)
            for name in module_names:
                try:
                    modules.append(import_module(name))
                except:
                    pass
                    '''
                    print >> sys.stderr, 'Exception occurred while loading module: %s' % name
                    traceback.print_exc()
                    print >> sys.stderr
                    '''
        if modified_path == 1:
            remove_sys_path(folder)

    return modules
    
def get_plugins(folder="plugins"):
    plugins = []
    
    for module in get_modules(folder):
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            try:
                if inspect.isclass(attr) and issubclass(attr, Plugin) and attr_name != 'Plugin':
                    plugins.append(attr())
            except Exception, e:
                print e
    return plugins
