import codecs
import json
import os

CONFIG = 'config.json'
BASE_PATH = os.path.join(os.path.dirname(__file__), '..')

def _(path):
    return path.replace('/', os.path.sep)

def load_config():
    content = load_file(os.path.join(BASE_PATH, CONFIG))
    return json.loads(content)

def save_config(dict):
    content = json.dumps(dict)
    save_file(os.path.join(BASE_PATH, CONFIG), content)

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
            base_path = BASE_PATH

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

    def __str__(self):
        return '<Resource "%s">'%self.path
    __repr__ = __str__

if __name__ == '__main__':
    print os.path.dirname(__file__)