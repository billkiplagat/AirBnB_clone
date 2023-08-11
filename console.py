#!/usr/bin/python3
"""program called console.py that contains the
entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """definition of class represinting interpreter"""

    prompt = "(hbnb) "

    def do_quit(self, line):
        """exit the program"""
        return True

    def do_EOF(self, line):
        """exit the program"""
        return True

    def emptyline(self):
        """overrides default emptyline method"""
        pass

    def do_help(self, line):
        """overrides help method"""
        cmd.Cmd.do_help(self, line)

    def do_create(self, line):
        """Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id"""
        if not line or len(line.split()) > 1:
            print("** class name missing **")
        elif line != "BaseModel":
            print("** class doesn't exist **")
        else:
            cls_instance = BaseModel()
            print(cls_instance.id)
            cls_instance.save()

    def do_show(self, line):
        """Prints the string representation of
        an instance based on the class name and id"""
        if not line:
            print("** class name missing **")
        else:
            command = line.split()
            if command[0] != "BaseModel":
                print("** class doesn't exist **")
            elif command[0] == "BaseModel" and len(command) == 1:
                print("** instance id missing **")
            try:
                storage = FileStorage()
                storage.reload()
                objs_dict = storage.all()
                instance = objs_dict[".".join(command)]
                print(instance)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and
        id (save the change into the JSON file)"""
        if not line:
            print("** class name missing **")
        else:
            command = line.split()
            if command[0] != "BaseModel":
                print("** class doesn't exist **")
            elif command[0] == "BaseModel" and len(command) == 1:
                print("** instance id missing **")
            try:
                storage = FileStorage()
                storage.reload()
                objs_dict = storage.all()
                del objs_dict[".".join(command)]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        """Prints all string representation of all
        instances based or not on the class name"""
        if line:
            command = line.split()
            if command[0] != "BaseModel" or len(command) > 1:
                print("** class doesn't exist **")
        storage = FileStorage()
        storage.reload()
        objs_dict = storage.all()
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
            if args[0] != "BaseModel":
                print("** class doesn't exist **")
            elif len(args) < 2:
                print("** instance id missing **")
            elif len(args) < 3:
                print("** attribute name missing **")
            elif len(args) < 4:
                print("** value missing **")
            else:
                try:
                    storage = FileStorage()
                    storage.reload()
                    objs_dict = storage.all()
                    instance = objs_dict[".".join(args[:2])]
                    attr_name = (args[2]).strip('"')
                    attr_value = args[3].strip('"')
                    if hasattr(instance, attr_name):
                        current_value = getattr(instance, attr_name)
                        attr_type = type(current_value)
                        try:
                            if attr_type == str:
                                setattr(instance, attr_name, attr_value)
                            elif attr_type == int:
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


if __name__ == '__main__':
    HBNBCommand().cmdloop()
