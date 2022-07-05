from pathlib import Path
import os
import sys
from source_files import *

os.system("color")

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

"""
System Arguments
mode app_name 
mode: test
app_name: any value

Proposed:
mode app_name db_option user_auth models 
"""

def main(*args):

    arguments = _arg_handler(args)
    print("arguments", args[0])
    print("dictionary", arguments)

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


    # handling system arguments... TODO partition in its own function
    # for x in args:
    #     # X is a list of args starting with the .py file
    #     for y in x:
    #         if y.lower() == "test":
    #             if len(x) > 2:
    #                 app_name = x[2]
    #                 test_mode(app_name)
    #             else:
    #                 test_mode("flask_app")
    #             return
    #         elif len(x) > 1:
    #             app_name = x[1]
    #         else:
    #             app_name = "flask_app"


    print(COLOR["BLUE"], "Current working directory:", Path.cwd(), COLOR["ENDC"])

    #Writing server.py file in current directory
    print(COLOR["GREEN"], "Creating", "server.py file", COLOR["ENDC"])
    server = open("server.py", "w+")
    server.write(server_py(app_name))
    server.close()




    #creating the app folder and going into it
    print(COLOR["GREEN"], "Creating", f"{app_name} folder", COLOR["ENDC"])
    Path(app_name).mkdir()
    os.chdir(app_name)

    #creating the folders inside the app folder accorindg to MVC design
    print(COLOR["GREEN"], "Creating", f"{app_name}/config directory", COLOR["ENDC"])
    Path("config").mkdir()
    print(COLOR["GREEN"], "Creating", f"{app_name}/controllers directory", COLOR["ENDC"])
    Path("controllers").mkdir()
    print(COLOR["GREEN"], "Creating", f"{app_name}/models directory", COLOR["ENDC"])
    Path("models").mkdir()
    print(COLOR["GREEN"], "Creating", f"{app_name}/static directory", COLOR["ENDC"])
    Path("static").mkdir()
    print(COLOR["GREEN"], "Creating", f"{app_name}/templates directory", COLOR["ENDC"])
    Path("templates").mkdir()

    #writing the __init__.py file for the module
    print(COLOR["GREEN"], "Creating", "__init__.py file", COLOR["ENDC"])
    module_file = open("__init__.py", "w+")
    module_file.write(APP_MODULE_FILE)
    module_file.close()

    #Going into the config directory to write the mysqlconnection.py file
    os.chdir("config")
    print(COLOR["GREEN"], "Creating", "config/mysqlconnection.py file", COLOR["ENDC"])
    mysql = open("mysqlconnection.py", "w+")
    #this .py file is responsible for connecting the app to the MySQL server
    mysql.write(MYSQLCONNECTION)
    mysql.close()
    #finished
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
    arguments ={}
    for idx, arg in enumerate(sys_args):
        try:
            if str(arg) == "-md":
                arguments["mode"] = sys_args[idx+1]
            elif arg == "-a":
                arguments["app_name"] = sys_args[idx+1]
            elif arg == "-db":
                arguments["database"] = sys_args[idx+1]
        except:
            arguments["error"] = "You may have entered invalid options:"
    if len(sys_args) > 1:
        if sys_args[1].lower() == "test":
            arguments["mode"] = "test"
        elif sys_args[1].lower() == "help":
            arguments["mode"] = "help"
    return arguments

def _test_mode(app_name):
    #check file paths
    print(COLOR["BLUE"], "TESTMODE:\nCurrent working directory:", Path.cwd(), COLOR["ENDC"], "\n")
    errors=[]
    tree = {
        app_name : ["config", "controllers", "models", "static", "templates", "__init__.py"],
        "server.py" : None
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
        this_error = COLOR["RED"]+mysqlcon +" already exists"+COLOR["ENDC"]
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

if __name__=="__main__":
    main(sys.argv)