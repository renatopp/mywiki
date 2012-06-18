import codecs
import json
import os

CONFIG = 'config.json'

def _(path):
    return path.replace('/', os.path.sep)

def load_config():
    content = load_file(CONFIG)
    return json.loads(content)

def save_config(dict):
    content = json.dumps(dict)
    save_file(CONFIG, content)

def load_file(file_path):
    file_ = codecs.open(_(file_path), 'r', 'utf-8')
    content = file_.read()
    file_.close()

    return content

def save_file(file_path, content):
    file_ = codecs.open(_(file_path), 'w', 'utf-8')
    file_.write(content)
    file_.close()


class Resource(object):
    def __init__(self, base_path=None, move_path=None):
        if base_path is None:
            base_path = os.path.dirname(__file__)

        self.__base_path = self.__split(base_path)
        self.__full_path = self.__base_path[:]
        self.__path = []
        self.__dirs = []
        self.__files = []
        self.__crumbs = []

        if move_path:
            self.move(move_path)

    def move(self, path, reset=False):
        self.__dirs = []
        self.__files = []
        self.__crumbs = []
        if reset:
            self.__path = []

        self.__path = self.__make_path(self.__path + self.__split(path))
        self.__full_path = self.__base_path + self.__path

    def join(self, *args):
        return self.__join(self.__make_path(self.__path+list(args)))

    def os_join(self, *args):
        return self.__os_join(self.__make_path(self.__full_path+list(args)))

    @property
    def crumbs(self):
        if not self.__crumbs:
            crumb = []
            for path in self.__path:
                crumb.append(self.__join([crumb[-1], path]) if crumb else path)
            self.__crumbs = crumb

        return self.__crumbs

    @property
    def path(self):
        return '/'.join(self.__path)

    @property
    def os_path(self):
        return os.path.sep.join(self.__full_path)

    @property
    def cur_dir(self):
        if self.is_file(): 
            if len(self.__path) <= 1:
                return 'home'
            else:
                return self.__path[-2]
        else:
            if len(self.__path) >= 1:
                return self.__path[-1]
            else:
                return 'home'

    @property
    def cur_file(self):
        if self.is_file():
            return self.__path[-1]
        else:
            return ''

    def is_base(self):
        return len(self.__path) == 0

    def is_dir(self):
        return os.path.isdir(self.os_path)

    def is_file(self):
        return os.path.isfile(self.os_path)

    def get_dirs(self):
        if not self.__dirs:
            self.__walk()
        
        return self.__dirs

    def get_files(self):
        if not self.__files:
            self.__walk()
            
        return self.__files

    def __join(self, path):
        return '/'.join(path)

    def __os_join(self, path):
        return os.path.sep.join(path)

    def __make_path(self, path):
        new = []
        for token in path:
            if token == '..' and new:
                new.pop()
            elif token != '.':
                new.append(token)

        return new

    def __walk(self):
        try:
            _, self.__dirs, self.__files = os.walk(self.os_path).next()
        except StopIteration as e:
            pass

    def __split(self, path):
        return path.replace('\\', '/').strip('/').split('/')

if __name__ == '__main__':
    path = '/dir 1/New Folder/a'
    # path = None
    resource = Resource('C:\\Users\\Renato\\Desktop\\wiki\\src', path)
    # resource.move('/../../3.rst')
    print '_Resource__path      :', resource._Resource__path
    print '_Resource__base_path :', resource._Resource__base_path
    print '_Resource__full_path :', resource._Resource__full_path
    print 'path                 :', resource.path
    print 'os_path              :', resource.os_path
    print 'cur_dir              :', resource.cur_dir
    print 'cur_file             :', resource.cur_file
    print 'is_base()            :', resource.is_base()
    print 'is_dir()             :', resource.is_dir()
    print 'is_file()            :', resource.is_file()
    print 'get_dirs()           :', resource.get_dirs()
    print 'get_files()          :', resource.get_files()
    print 'join                 :', resource.join('_____')
    print 'os_join              :', resource.os_join('_____')
    print 'crumbs               :', resource.crumbs