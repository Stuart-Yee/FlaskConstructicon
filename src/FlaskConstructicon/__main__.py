from pathlib import Path
import os
from sys import argv
from resources import *
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

MVC_TREE = {
    "files": {"server.py": "server.py"},
    "directories": {
            "app_name": {
                "files": {"__init__.py": "app_module_file"},
                "directories": {
                    "config": {
                        "files": {"mysqlconnection.py": "mysqlconnection"},
                        "directories": None
                    },
                    "models": {"files": None, "directories": None},
                    "controllers": {"files": None, "directories": None},
                    "static": {"files": None, "directories": None},
                    "templates": {"files": None, "directories": None},
                    "ext_apis": {"files": None, "directories": None}
            }
        }
    }
}


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
        _test_mode(app_name, MVC_TREE, os.getcwd())
        return

    print(COLOR["BLUE"], "Current working directory:", Path.cwd(), COLOR["ENDC"])
    _build_mvc_pattern(app_name, arguments)


def _build_mvc_pattern(app_name, arguments):
    # Writing server.py file in current directory
    try:
        print(COLOR["GREEN"], "Creating", "server.py file", COLOR["ENDC"])
        server = open("server.py", "w+")
        print(MVC_TREE["files"][0][1])
        server.write(server_py(app_name))
        server.close()
    except Exception as e:
        print(COLOR["RED"], str(e), COLOR["ENDC"])

    # creating the app folder and going into it
    try:
        print(COLOR["GREEN"], "Creating", f"{app_name} folder", COLOR["ENDC"])
        Path(app_name).mkdir()
    except Exception as e:
        print(COLOR["RED"], str(e), COLOR["ENDC"])
    finally:
        os.chdir(app_name)

    # creating the folders inside the app folder accorindg to MVC design
    for directory in MVC_TREE["directories"][0]["app_name"]["directories"]:
        try:
            for dir_name, value in directory.items():
                print(COLOR["GREEN"], "Creating", f"{app_name}/{dir_name} directory", COLOR["ENDC"])
                Path(dir_name).mkdir()
        except Exception as e:
            print(COLOR["RED"], str(e), COLOR["ENDC"])

    # writing the __init__.py file for the module
    print(COLOR["GREEN"], "Creating", "__init__.py file", COLOR["ENDC"])
    module_file = open("__init__.py", "w+")
    module_file.write(VAULT.get("APP_MODULE_FILE"))
    module_file.close()

    # Going into the config directory to write the mysqlconnection.py file
    if arguments.get("database") == "mysql":
        os.chdir("config")
        print(COLOR["GREEN"], "Creating", "config/mysqlconnection.py file", COLOR["ENDC"])
        mysql = open("mysqlconnection.py", "w+")
        # this .py file is responsible for connecting the app to the MySQL server
        mysql.write(MYSQLCONNECTION)
        mysql.close()
        # finished

    print(COLOR["BLUE"], "Directories and files for your Flask project successfully created", COLOR["ENDC"])
    return


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
def _inner_loop(app_name, pattern, current_path):
    errors = []
    curr_dir = str(os.getcwd())
    if pattern["files"]:
        for file in pattern["files"]:
            abs_path = os.path.join(current_path, file)
            sub_path = str(abs_path).replace(curr_dir, ".")
            if os.path.exists(abs_path):
                this_error = COLOR["RED"] + sub_path + " already exists" + COLOR["ENDC"]
                print(this_error)
                errors.append(this_error)
            else:
                print(COLOR["GREEN"], sub_path, " doesn't exist", COLOR["ENDC"])
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
            errors += _inner_loop(app_name, pattern["directories"][old_key], abs_path)
    return errors


def _test_mode(app_name, pattern, current_path):
    print(COLOR["BLUE"], "TESTMODE:\nCurrent working directory:", Path.cwd(), COLOR["ENDC"], "\n")

    errors = _inner_loop(app_name, pattern, current_path)

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
