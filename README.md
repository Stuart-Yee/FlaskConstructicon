# FlaskConstructicon
![image](https://user-images.githubusercontent.com/75331586/177195753-b57551ca-c7ab-4299-9b7d-8da8c0b321f5.png)

Flask Project Builder

Constructs a file tree for Flask with a server.py file parallel to the `flask_app` directory:

![image](https://user-images.githubusercontent.com/75331586/177196250-5b0ae026-6562-4c08-b999-96f47b3374c9.png)

# Simple Install:
1) Clone this Repository

# Simple Usage:
1) Navigate to your new directory's project
2) Run FlaskConstructicon.py
`>> python path/to/FlaskConstructicon.py [system arguments]`
3) FlaskConstructicon takes one system argument, `test` to see if the current directory doesn't already have the files and directories FlaskConstructicon will write

# Use an alias
Example alias using git bash:
`alias constructicon='winpty python C:/Path/To/FlaskConstructicon/FlaskConstructicon.py'`

# Next steps:
-Externalise source files
-Enhance arg parcer (db connection options)
-Add source files for other db connections and/or APIs
-publish package