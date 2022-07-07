# FlaskConstructicon
![image](https://user-images.githubusercontent.com/75331586/177195753-b57551ca-c7ab-4299-9b7d-8da8c0b321f5.png)

Flask Project Builder

Constructs a file tree for Flask with a server.py file parallel to the `flask_app` directory:

![image](https://user-images.githubusercontent.com/75331586/177196250-5b0ae026-6562-4c08-b999-96f47b3374c9.png)

Installation:
1) `pip install flaskconstructicon`

# Simple Usage:
1) Navigate to your new directory's project
2) Run FlaskConstructicon
`>> python -m flaskconstructicon [system arguments]`
3) FlaskConstructicon takes several arguments 

<table>
    <thead>
        <tr>
            <th>Argument</th>
            <th>Options</th>
            <th>Description</th>
            <th>Examples</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>-md</td>
            <td>test, help</td>
            <td>Run mode, test or help</td>
            <td>python FlaskConstructicon.py -md test</td>
        </tr>
        <tr>
            <td>-a</td>
            <td>Any</td>
            <td>Specifies app name</td>
            <td>python FlaskConstructicon.py -a my_app</td>
        </tr>
        <tr>
            <td>-db</td>
            <td>mysql</td>
            <td>Add file for database API</td>
            <td>python FlaskConstructicon.py -db mysql</td>
        </tr>
        <tr>
            <td>test</td>
            <td>N/A</td>
            <td>Same as -md test (first argument only)</td>
            <td>python FlaskConstructicon.py test</td>
        </tr>
        <tr>
            <td>help</td>
            <td>N/A</td>
            <td>Same as -md help (first argument only)</td>
            <td>python FlaskConstructicon.py help</td>
        </tr>
    </tbody>
</table>

<h3>Test output with app name 'simflario'</h3>

![image](https://user-images.githubusercontent.com/75331586/177251274-b439eb82-0787-4179-a4b2-ca8bf2b981f2.png)

<h3>Output creating new project:</h3>

![image](https://user-images.githubusercontent.com/75331586/177251369-0f797d52-c371-4aba-a914-9762cc7c141a.png)

<h3>Test output with existing project</h3>

![image](https://user-images.githubusercontent.com/75331586/177251447-4dcc19a0-05fa-4f92-ba1f-09563d31a280.png)


# Use an alias
Example alias using git bash:
`alias constructicon='winpty python C:/Path/To/FlaskConstructicon/FlaskConstructicon.py'`

# Next steps:

>-Add source files for other db connections and/or APIs

>-create models files and models option

>-create "Django Style" option

>-create option `dbua` for user model and authentication based on db config
