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



def main(*args):
    # handling system arguments... TODO partition in its own function
    for x in args:
        # X is a list of args starting with the .py file
        for y in x:
            if y.lower() == "test":
                if len(x) > 2:
                    app_name = x[2]
                    test_mode(app_name)
                else:
                    test_mode("flask_app")
                return
            elif len(x) > 1:
                app_name = x[1]
            else:
                app_name = "flask_app"


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
    module_file.write(
"from flask import Flask, session\napp = Flask(__name__)\napp.secret_key = \"YOUR SECRET KEY\"\n#TODO Change secret key"
)
    module_file.close()

    #Going into the config directory to write the mysqlconnection.py file
    os.chdir("config")
    print(COLOR["GREEN"], "Creating", "config/mysqlconnection.py file", COLOR["ENDC"])
    mysql = open("mysqlconnection.py", "w+")
    #this .py file is responsible for connecting the app to the MySQL server
    mysql.write(
"# a cursor is the object we use to interact with the database\nimport pymysql.cursors\n# this class will give us an instance of a connection to our database\nclass MySQLConnection:\n\tdef __init__(self, db):\n\t\t# change the user and password as needed\n\t\tconnection = pymysql.connect(host='localhost', user='root', password='root', db=db, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, autocommit=True)\n\t\t# establish the connection to the database\n\t\tself.connection = connection\n\t# the method to query the database\n\tdef query_db(self, query, data=None):\n\t\twith self.connection.cursor() as cursor:\n\t\t\ttry:\n\t\t\t\tquery = cursor.mogrify(query, data)\n\t\t\t\tprint(\"Running Query:\", query)\n\t\t\t\texecutable = cursor.execute(query, data)\n\t\t\t\tif query.lower().find(\"insert\") >= 0:\n\t\t\t\t\t# INSERT queries will return the ID NUMBER of the row inserted\n\t\t\t\t\tself.connection.commit()\n\t\t\t\t\treturn cursor.lastrowid\n\t\t\t\telif query.lower().find(\"select\") >= 0:\n\t\t\t\t\t# SELECT queries will return the data from the database as a LIST OF DICTIONARIES\n\t\t\t\t\tresult = cursor.fetchall()\n\t\t\t\t\treturn result\n\t\t\t\telse:\n\t\t\t\t\t# UPDATE and DELETE queries will return nothing\n\t\t\t\t\tself.connection.commit()\n\t\t\texcept Exception as e:\n\t\t\t\t# if the query fails the method will return FALSE\n\t\t\t\tprint(\"Something went wrong\", e)\n\t\t\t\treturn False\n\t\t\tfinally:\n\t\t\t\t# close the connection\n\t\t\t\tself.connection.close()\n\t\t\t\t# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection\ndef connectToMySQL(db):\n\treturn MySQLConnection(db)")
    mysql.close()
    #finished
    print(COLOR["BLUE"], "Directories and files for your Flask project successfully created", COLOR["ENDC"])
    return

def help():
    #TODO print help items
    pass

def arg_handler(*args):
    #TODO route argements
    pass

def test_mode(app_name):
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