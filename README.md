# Flask Base Template

This is a base template created for Flask designed to allow for a quicker start to future projects.  See a deploy version at https://flask-base-template.herokuapp.com/.

## Features

- Flask project base file structure
- Base template structure w/ navbar and Bootstrap
- Procfile & gunicorn for quick Heroku deployment

## Contents

- [Setup](#Setup)
- [Built With](#built-with)

## Setup

To get this up and running quickly follow these steps:

On Github, click "Use this template" and create a new repo:
![image](https://user-images.githubusercontent.com/33850990/89134476-303e1700-d4eb-11ea-87df-02e00ddbcb0d.png)

In a fresh folder on your computer, start up git:
```
git init
```

Pull in the repo you just created:
```
git pull INSERT_REPO_URL_HERE
```

Install virtualenv if you don't have it already and set up the environment (in the root folder still):
```
pip install virtual env
```
```
python -m virtualenv venv
```
Activate the virtual environment:
```
venv\scripts\activate
```

Now install the requirements.txt (currently this is just Flask 1.1.2):
```
pip install -r requirements.txt
```

You will need to create your own secret key in order to get things up and running.  The project will try to import a file called ```local_settings.py``` which should be created at ```project/local_settings.py```.  Once made add the following lines to it:
```
import os

os.environ['SECRET_KEY'] = 'INSERT_SECRET_KEY_HERE'
```

You can create a new secret key from running the following code in a python shell:
```
>>> import uuid
>>> uuid.uuid4().hex
`1f60e76982584005ac1140bbc6013234`
```

Once this is done you should be able to get things rolling, set your FLASK_APP environment variable (for Windows):
```
set FLASK_APP=run.py
```

Now run the app:
```
flask run
```

Navigate to ```127.0.0.1:5000``` in your browser and you should now see the page loaded. Great job!

## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - for the webserver
- [Bootstrap](https://getbootstrap.com/docs/4.0/getting-started/introduction/) - for quick and easy responsive CSS & Javascript