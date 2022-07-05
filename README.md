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

![image](https://user-images.githubusercontent.com/75331586/177205506-3f16de96-5529-4477-9389-3990d98a17e5.png)

<h3>Output creating new project:</h3>

![image](https://user-images.githubusercontent.com/75331586/177205567-201293c7-ff16-4b6a-94ab-d86dc46361bd.png)

<h3>Test output with existing project</h3>

![image](https://user-images.githubusercontent.com/75331586/177206044-cb80e453-f0b1-41d8-bb93-112852821a57.png)


# Use an alias
Example alias using git bash:
`alias constructicon='winpty python C:/Path/To/FlaskConstructicon/FlaskConstructicon.py'`

# Next steps:
>-Externalise source files

>-Enhance arg parcer (db connection options)

>-Add source files for other db connections and/or APIs

>-publish package
