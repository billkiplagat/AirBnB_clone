#!/usr/bin/python3
"""program called console.py that contains the
entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import sys
import re


class HBNBCommand(cmd.Cmd):
    """definition of class representing interpreter"""

    prompt = "(hbnb) "

    class_map = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def precmd(self, line):
        """modifies the input command"""
        l_list = line.split(".")
        if len(l_list) == 2:
            if l_list[0] in self.class_map and l_list[1] == "all()":
                return "all " + l_list[0]
            elif l_list[0] in self.class_map and l_list[1] == "count()":
                return "count " + l_list[0]
            elif l_list[0] in self.class_map and l_list[1].split(
                    '("')[0] == "show":
                id = l_list[1][5:-1]
                return "show_id " + id
            elif l_list[0] in self.class_map and l_list[1].split(
                    '("')[0] == "destroy":
                id = l_list[1][8:-1]
                return "destroy_id " + id
            elif l_list[0] in self.class_map and l_list[1].split(
                    '("')[0] == "update":
                args = l_list[1][7:-1].split(", ")
                if "{" not in args[1]:
                    return "update " + l_list[0] + " " + " ".join(args)
                else:
                    args = l_list[1][7:-2].split(", {")
                    id = args[0].strip("'")
                    attr_list = args[1].split(", ")
                    first_attr = attr_list[0].split(": ")
                    attr_one = [attr.strip("'") for attr in first_attr]
                    second_attr = attr_list[1].split(": ")
                    attr_two = [attr.strip("'") for attr in second_attr]
                    result = " ".join(attr_one) + " " + " ".join(attr_two)
                    return "update " + l_list[0] + " " + id + " " + result
            else:
                return line
        else:
            return line

    def do_quit(self, line):
        """exit the program"""
        return True

    def do_EOF(self, line):
        """exit the program"""
        return True

    def emptyline(self):
        """overrides default empty line method"""
        pass

    def do_help(self, line):
        """overrides help method"""
        cmd.Cmd.do_help(self, line)

    def do_create(self, line):
        """Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id"""
        if not line or len(line.split()) > 1:
            print("** class name missing **")
        elif line not in self.class_map:
            print("** class doesn't exist **")
        else:
            for key, value in self.class_map.items():
                if key == line:
                    cls_instance = value()
            print(cls_instance.id)
            cls_instance.save()

    def do_show(self, line):
        """Prints the string representation of
        an instance based on the class name and id"""
        if not line:
            print("** class name missing **")
        else:
            command = line.split()
            if command[0] not in self.class_map:
                print("** class doesn't exist **")
            elif command[0] in self.class_map and len(command) == 1:
                print("** instance id missing **")
            try:
                objs_dict = storage.all()
                instance = objs_dict[".".join(command)]
                print(instance)
            except KeyError:
                print("** instance id missing **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and
        id (save the change into the JSON file)"""
        if not line:
            print("** class name missing **")
        else:
            command = line.split()
            if command[0] not in self.class_map:
                print("** class doesn't exist **")
            elif command[0] in self.class_map and len(command) == 1:
                print("** instance id missing **")
            try:
                objs_dict = storage.all()
                del objs_dict[".".join(command)]
                storage.save()
            except KeyError:
                print("** instance id missing **")

    def do_all(self, line):
        """Prints all string representation of all
        instances based or not on the class name"""
        objs_dict = storage.all()
        if line:
            command = line.split()
            if command[0] not in self.class_map or len(command) > 1:
                print("** class doesn't exist **")
            else:
                if objs_dict:
                    for key, value in objs_dict.items():
                        if key.split('.')[0] == command[0]:
                            print(value)
        else:
            if objs_dict:
                for key, value in objs_dict.items():
                    print(value)

    def do_update(self, line):
        """ Updates an instance based on the class name and id by adding
        or updating attribute (save the change into the JSON file)"""
        if not line:
            print("** class name missing **")
        else:
            args = line.split()
            if args[0] not in self.class_map:
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                try:
                    objs_dict = storage.all()
                    id = ".".join([args[0].strip('"'), args[1].strip('"')])
                    instance = objs_dict[id]
                    attr_name = (args[2]).strip('"')
                    attr_value = args[3].strip('"')
                    if hasattr(instance, str(attr_name)):
                        current_value = getattr(instance, attr_name)
                        attr_type = type(current_value)
                        try:
                            if attr_type == str:
                                setattr(instance, attr_name, attr_value)
                            elif attr_type == int:
                                print(attr_name)
                                setattr(instance, attr_name, int(attr_value))
                            elif attr_type == float:
                                setattr(instance, attr_name, float(attr_value))
                        except ValueError:
                            print("** invalid value for attribute **")
                    else:
                        setattr(instance, attr_name, attr_value)
                    storage.save()
                except KeyError:
                    print("** no instance found **")

    def do_count(self, line):
        """retrieve the number of instances
        of a class: <class name>.count()"""
        objs_dict = storage.all()
        count = 0
        for key in objs_dict.keys():
            if key.split(".")[0] == line:
                count += 1
        print(count)

    def do_show_id(self, line):
        """retrieve an instance based on its ID: <class name>.show(<id>)"""
        objs_dict = storage.all()
        found = False
        for key, value in objs_dict.items():
            if key.split(".")[1] == line.strip('"'):
                print(value)
                found = True
        if not found:
            print("** no instance found **")

    def do_destroy_id(self, line):
        """destroy an instance based on its ID: <class name>.show(<id>)"""
        objs_dict = storage.all()
        found = False
        for key in list(objs_dict.keys()):
            if key.split(".")[1] == line.strip('"'):
                del objs_dict[key]
                found = True
        if found:
            storage.save()
        else:
            print("** no instance found **")

    def postcmd(self, stop, line):
        """Execute after each command"""
        if line.startswith("update"):
            cmd_args = line.split()
            if len(cmd_args) > 5 and cmd_args[1] in self.class_map:
                cmd_args.pop(3)
                cmd_args.pop(3)
                cmd_args = [item.strip('"') for item in cmd_args]
                update_cmd = " ".join(cmd_args)
                self.onecmd(update_cmd)
        return stop


if __name__ == "__main__":
    HBNBCommand().cmdloop()
