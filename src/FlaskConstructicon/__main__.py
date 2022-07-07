from pathlib import Path
import os
from sys import argv
from resources import *
from pprint import pprint

os.system("color")

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

MVC_TREE = {
    "top": {
        "files": ["server.py"],
        "directories": [
            {
                "app_name": {
                    "files": ["__init__.py"],
                    "directories": [
                        {"config": {"files": [], "directories": []}},
                        {"models": {"files": [], "directories": []}},
                        {"controllers": {"files": [], "directories": []}},
                        {"static": {"files": [], "directories": []}},
                        {"templates": {"files": [], "directories": []}},
                        {"ext_apis": {"files": [], "directories": []}}
                    ]
                }
            }
        ]
    }
}


def main(*args):
    arguments = _arg_handler(args)

    if arguments.get("error"):
        print(COLOR["RED"], arguments.get("error"), COLOR["ENDC"])
        cli = ""
        for arg in args[0][1:]:
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
        _test_mode(app_name)
        return

    print(COLOR["BLUE"], "Current working directory:", Path.cwd(), COLOR["ENDC"])
    _build_mvc_pattern(app_name, arguments)


def _build_mvc_pattern(app_name, arguments):
    # Writing server.py file in current directory
    try:
        print(COLOR["GREEN"], "Creating", "server.py file", COLOR["ENDC"])
        server = open("server.py", "w+")
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
    for directory in MVC_TREE["top"]["directories"][0]["app_name"]["directories"]:
        try:
            for dir_name, value in directory.items():
                print(COLOR["GREEN"], "Creating", f"{app_name}/{dir_name} directory", COLOR["ENDC"])
                Path(dir_name).mkdir()
        except Exception as e:
            print(COLOR["RED"], str(e), COLOR["ENDC"])

    # writing the __init__.py file for the module
    print(COLOR["GREEN"], "Creating", "__init__.py file", COLOR["ENDC"])
    module_file = open("__init__.py", "w+")
    module_file.write(APP_MODULE_FILE)
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


def _arg_handler(*args):
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

    sys_args = args[0][0]
    arguments = {}
    for idx, arg in enumerate(sys_args):
        try:
            if str(arg) == "-md":
                arguments["mode"] = sys_args[idx + 1]
            elif arg == "-a":
                arguments["app_name"] = sys_args[idx + 1]
            elif arg == "-db":
                arguments["database"] = sys_args[idx + 1]
                if arguments["database"] not in SUPPORTED_DATABASES:
                    arguments["error"] = f"{arguments['database']} is not a supported database"
        except:
            arguments["error"] = "You may have entered invalid options:"
    if len(sys_args) > 1:
        if sys_args[1].lower() == "test":
            arguments["mode"] = "test"
        elif sys_args[1].lower() == "help":
            arguments["mode"] = "help"
    return arguments


def _test_mode(app_name, pattern=None):
    # check file paths
    print(COLOR["BLUE"], "TESTMODE:\nCurrent working directory:", Path.cwd(), COLOR["ENDC"], "\n")
    errors = []
    tree = {
        app_name : ["config", "controllers", "models", "static", "templates", "__init__.py"],
        "server.py": None
    }
    for top in tree.keys():
        if(os.path.exists(os.path.join(os.getcwd(),top))):
            this_error = COLOR["RED"]+top+" already exists"+COLOR["ENDC"]
            errors.append(this_error)
            print(this_error)
        else:
            print(COLOR["GREEN"], top, " doesn't exist", COLOR["ENDC"])
        if tree[top]:
            for sub in tree[top]:
                sub_path = os.path.join(top, sub)
                abs_path = os.path.join(os.getcwd(), sub_path)
                if(os.path.exists(abs_path)):
                    this_error = COLOR["RED"]+sub_path+" already exists"+COLOR["ENDC"]
                    print(this_error)
                    errors.append(this_error)
                else:
                    print(COLOR["GREEN"], sub_path, " doesn't exist", COLOR["ENDC"])

    mysqlcon = os.path.join(app_name, "config", "mysqlconnection.py")
    if os.path.exists(os.path.join(os.getcwd(), mysqlcon)):
        this_error = COLOR["RED"] + mysqlcon + " already exists" + COLOR["ENDC"]
        errors.append(this_error)
        print(this_error)
    else:
        print(COLOR["GREEN"], mysqlcon, " doesn't exist", COLOR["ENDC"])

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
