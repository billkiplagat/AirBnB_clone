#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split

from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_quit(self, args):
        """Exit the command interpreter"""
        return True

    def do_EOF(self, args):
        """Exit the command interpreter by pressing Ctrl+D (EOF)"""
        print("")
        return True

    def do_help(self, args):
        """Display help message"""
        cmd.Cmd.do_help(self, args)

    def emptyline(self):
        """Do nothing for an empty line"""
        pass

    def do_create(self, line):
        """Usage: create <class> <key 1>=<value 2> <key 2>=<value 2> ...
        Create a new class instance with given keys/values and print its id.
        """
        try:
            if not line:
                raise SyntaxError()
            my_list = line.split(" ")

            kwargs = {}
            for i in range(1, len(my_list)):
                key, value = tuple(my_list[i].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = value
            if kwargs == {}:
                obj = eval(my_list[0])()
            else:
                obj = eval(my_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")

        except NameError:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
