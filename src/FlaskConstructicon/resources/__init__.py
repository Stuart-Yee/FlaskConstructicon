from os import path, walk

BASE = path.dirname(__file__)

SUPPORTED_DATABASES = ("mysql")

APP_MODULE_FILE = """
from flask import Flask, session\n
app = Flask(__name__)\n
app.secret_key = \"YOUR SECRET KEY\"\n
#TODO Change secret key
"""

# Build server.py based on app name
def server_py(app_name="flask_app"):
    print("running from __init__")
    return f"""
from {app_name}.controllers import #TODO controllers go here\n
from {app_name} import app\n
if __name__==\"__main__\":\n
\tapp.run(debug=True)
"""

# File builder from .txt
def _file_from_text(file_name):
    with open(path.join(BASE, file_name), "r") as file:
        text = file.read()
    return text

TEST_TEXT = _file_from_text("test.txt")

HELP = _file_from_text("help.txt")

MYSQLCONNECTION = _file_from_text("database_configs/mysqlconnection.txt")

MODELS = []
for (dirpath, dirname, fnames ) in walk(path.join(BASE, "models")):
    MODELS.extend(fnames)

VAULT = {
    "app_module_file": APP_MODULE_FILE,
    "mysqlconnection": MYSQLCONNECTION,
}
