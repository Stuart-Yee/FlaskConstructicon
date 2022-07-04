SERVER_PY_DEFAULT = """
from flask_app.controllers import #TODO controllers go here\n
from flask_app import app\n
if __name__==\"__main__\":\n
\tapp.run(debug=True)
"""

def server_py(app_name="flask_app"):
    return f"""
    from {app_name}.controllers import #TODO controllers go here\n
    from {app_name} import app\n
    if __name__==\"__main__\":\n
    \tapp.run(debug=True)
    """