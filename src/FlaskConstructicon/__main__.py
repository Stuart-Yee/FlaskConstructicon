from pathlib import Path
import os
from sys import argv
from .resources import *
from pprint import pprint

os.system("color")

app_name = "smelly"

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

"""
File pattern is a JSON with sets keys "files" and "directories".
The value for "files" is a dictionary with the filename as the key
and the value serving as a key for the VAULT in the resources __init__.py

"directories" is recursive having a key being the directory name and its
value being a recursive nesting of more "files" and "directories"

As of 7/10/2022 only one pattern is supported based on the design pattern
taught at Coding Dojo.

Future design patterns will be added and stored in resources as a .JSON
"""

def main(args):
    arguments = _arg_handler(args)

    if arguments.get("error"):
        print(COLOR["RED"], arguments.get("error"), COLOR["ENDC"])
        cli = ""
        for arg in args[1:]:
            cli += arg + " "
        print("ARGUMENTS:", cli)
        print(COLOR["GREEN"], HELP, COLOR["ENDC"])
        return

    if arguments.get("app_name"):
        app_name = arguments["app_name"]
    else:
        app_name = "flask_app"

    if arguments.get("mode") == "help":
        print(COLOR["GREEN"], HELP, COLOR["ENDC"])
        return
    elif arguments.get("mode") == "test":
        _test_mode(app_name, CD_MVC, os.getcwd(), arguments)
        return

    print(COLOR["BLUE"], "Current working directory:", Path.cwd(), COLOR["ENDC"], "\n")
    errors = _inner_loop(app_name, CD_MVC, os.getcwd(), arguments, test=False)
    if len(errors) > 0:
        for error in errors:
            print(COLOR["RED"], error, COLOR["ENDC"])
    else:
        print("\n", COLOR["BLUE"], "Directories and files for your Flask project successfully created", COLOR["ENDC"])

def _arg_handler(args):
    """
    System Arguments
    -md, mode --help, test
    -a app_name --any
    -db database --mysql

    Shortcuts (applies to first argument only):
    test - enters test mode
    help - enters help mode

    Future options
    -dbua user authentication, will build models and controllers for basic user authentication based on db
    -models build model files and controllers from source_files/models
    """

    arguments = {}
    for idx, arg in enumerate(args):
        try:
            if str(arg) == "-md":
                arguments["mode"] = args[idx + 1]
            elif arg == "-a":
                arguments["app_name"] = args[idx + 1]
            elif arg == "-db":
                arguments["database"] = args[idx + 1]
                if arguments["database"] not in SUPPORTED_DATABASES:
                    arguments["error"] = f"{arguments['database']} is not a supported database"
        except:
            arguments["error"] = "You may have entered invalid options:"
    if len(args) > 1:
        if args[1].lower() == "test":
            arguments["mode"] = "test"
        elif args[1].lower() == "help":
            arguments["mode"] = "help"
    return arguments


# new loops to support any provided pattern
def _inner_loop(app_name, pattern, current_path, arguments, test=True):
    errors = []
    curr_dir = str(os.getcwd())
    db = arguments.get("database")
    if pattern["files"]:
        for file, contents in pattern["files"].items():
            if (db == contents and contents in SUPPORTED_DATABASES) or contents not in SUPPORTED_DATABASES:
                abs_path = os.path.join(current_path, file)
                sub_path = str(abs_path).replace(curr_dir, ".")
                if os.path.exists(abs_path):
                    this_error = COLOR["RED"] + sub_path + " already exists" + COLOR["ENDC"]
                    print(this_error)
                    errors.append(this_error)
                else:
                    print(COLOR["GREEN"], sub_path, " doesn't exist", COLOR["ENDC"])
                    if not test:
                        print(COLOR["HEADER"], "Creating", sub_path, COLOR["ENDC"])
                        with open(abs_path, "w+") as new_file:
                            if file == "server.py":
                                new_file.write(server_py(app_name))
                            elif contents != "empty":
                                new_file.write(VAULT[contents])
    if pattern["directories"]:
        for dir_name in pattern["directories"]:
            old_key = dir_name
            if dir_name == "app_name":
                dir_name = app_name
            abs_path = os.path.join(current_path, dir_name)
            sub_path = str(abs_path.replace(curr_dir, "."))
            if os.path.exists(abs_path):
                this_error = COLOR["RED"] + sub_path + " already exists" + COLOR["ENDC"]
                print(this_error)
                errors.append(this_error)
            else:
                print(COLOR["GREEN"], sub_path, " doesn't exist", COLOR["ENDC"])
                if not test:
                    os.mkdir(abs_path)
                    print(COLOR["HEADER"], "Creating", f"{sub_path} directory", COLOR["ENDC"])

            errors += _inner_loop(app_name, pattern["directories"][old_key], abs_path, arguments, test=test)
    return errors


def _test_mode(app_name, pattern, current_path, arguments):
    print(COLOR["BLUE"], "TESTMODE:\nCurrent working directory:", Path.cwd(), COLOR["ENDC"], "\n")

    errors = _inner_loop(app_name, pattern, current_path, arguments)

    if len(errors) > 0:
        print("\n", COLOR["RED"], len(errors), " error(s):")
        for error in errors:
            print(error, COLOR["ENDC"])
    else:
        print(COLOR["GREEN"], "\nNo errors, ready to construct app file tree", COLOR["ENDC"])
    print(COLOR["BLUE"], "\nTEST MODE. TERMINATING SESSION", COLOR["ENDC"])
    return


if __name__ == "__main__":
    main(argv)
