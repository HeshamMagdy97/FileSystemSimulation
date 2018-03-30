from abc import ABCMeta, abstractmethod
import math


class IFileSystemElement:

    __metaclass__ = ABCMeta

    @abstractmethod
    def create_dir(self, root_name, name): pass

    @abstractmethod
    def create_file(self, root_name, name): pass

    @abstractmethod
    def remove_file(self, name): pass

    @abstractmethod
    def show(self): pass


class DirectoryComposite(IFileSystemElement):

    def __init__(self, name):
        self.__name = name
        self.__files = set()

    def check_found(self, name):
        if self.__name == name:
            return False
        for file in self.__files:
            if file.get_name():
                return False
        return True

    def show(self,indent):
        print(indent*" "+"| "+self.__name)
        for file in self.__files:
            file.show(indent + 2)

    def create_dir(self, root_name, name):
        if self.__name == root_name:
            self.__files.add(DirectoryComposite(name))
        for file in self.__files:
            file.create_dir(root_name,name)

    def create_file(self, root_name, name):
        if self.__name == root_name:
            self.__files.add(File(name))
        for file in self.__files:
            file.create_file(root_name,name)

    def remove_file(self, name):
        s = ""

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name


class File(IFileSystemElement):

    def __init__(self, name):
        self.__name = name
        self.__size = 0

    def show(self,intent):
        print(intent * " " + "-- " +self.__name)

    def create_file(self, root_name, name): pass

    def create_dir(self, root_name, name): pass

    def remove_file(self, name): pass

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_size(self):
        return self.__size

    def set_size(self, size):
        self.__size = size


class FileSystem:

    def __init__(self, disk_size, block_size):
        extent_size = math.ceil(disk_size / block_size)
        self.__extent = [x for x in range(0,extent_size)]
        print([x for x in self.__extent])
        self.__root = DirectoryComposite("root")
        self.__disk_size = disk_size
        self.__block_size = block_size

    def print_state(self):
        self.__root.show(1)

    def create_dir(self, name):
        names = name.split("/")
        if names[0] != "root":
            return False
        else:
            for title in names[1:-1]:
                if self.__root.check_found(title):
                    return False
            dir_name = names[len(names)-1]
            parent = names[len(names)-2]
            self.__root.create_dir(parent,dir_name)
            return True

    def create_file(self, name,size):
        names = name.split("/")
        if names[0] != "root" or size > self.__disk_size:
            return False
        else:
            for title in names[1:-1]:
                if self.__root.check_found(title):
                    return False
            dir_name = names[len(names)-1]
            parent = names[len(names)-2]
            self.__root.create_file(parent,dir_name)
            return True


vfs = FileSystem(200, 1)

while True:
    command = input("Enter the command").split()

    if command[0] == "CreateFile":
        vfs.create_file(command[1], int(command[2]))

    if command[0] == "CreateFolder":
        print(vfs.create_dir(command[1]))

    vfs.print_state()


