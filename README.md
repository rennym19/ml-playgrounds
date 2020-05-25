# ml-playgrounds
> Allows to upload and/or parse your datasets so that you can apply multiple Data Science, Statistics and Machine Learning techiques without having to write any code!

> Python, Django, Rest API, MongoDB, React, Data Science, Machine Learning

## Live Demo
Soon

## What does it look like?
<p align="center">
  <img src="https://raw.githubusercontent.com/rennym19/ml-playgrounds/master/docs/img/user-register.png" width="600px" alt="Signup page"/>
<p/>

<hr/>

## Getting Started
Running this project locally requires little to no setup, assuming you already have python3, pip3, virtualenv, node and npm installed. MongoDB is not necessary if you're planning on using Atlas, else, you're going to have to install and setup MongoDB server in your computer.

### Prerequisites
- [python3](https://www.python.org/download/releases/3.0/)
- pip3 (comes with python3)
- virtualenv (comes with python3)
- [mongodb server](https://www.mongodb.com/download-center/community)

### Installation
#### Back end setup
1. Clone this repo.
  ```
  git clone git@github.com:rennym19/ml-playgrounds.git
  ```
2. Create a new python virtual environment, activate it and install requirements.
  ```
  cd ml-playgrounds
  python3 virtualenv -m venv
  source venv/bin/activate
  pip3 install -r requirements.txt
  ```
3. Change database settings in mlplaygrounds/settings.py. If you're running locally, it may work as it is.
  ```
  ...
  DATABASES = {
    'default': {
      ...,
      'HOST': 'localhost', # Change this (if needed)
      'PORT': 27017, # And this (again, if needed)
    }
  }
  ...
  ```
4. Migrate database.
  ```
  python3 manage.py migrate
  ```

#### Front end setup:
Change directory to mlplaygrounds/frontend and install node dependencies.
  ```
  cd mlplaygrounds/frontend
  npm install
  ```

### Testing:
Go to the projects root directory and run:
  ```
  pytest
  ```
  
### Running:
Make sure your virtualenv is active and your DB service is running. Go to the projects root directory and run:
  ```
  python3 manage.py runserver
  ```

<hr/>

## Technical Details
As of now, the project is using the following technologies:
- [Python 3](https://www.python.org/) with the [Django framework](https://www.djangoproject.com/) in the back end.
- [Django Rest Framework](https://www.django-rest-framework.org/) to build the REST API.
- [Knox](https://github.com/James1345/django-rest-knox) for user token authentication.
- [Pytest](https://docs.pytest.org/en/latest/) and [unittest](https://docs.python.org/3/library/unittest.html) packages for Unit Tests in Python.
- [MongoDB](https://www.mongodb.com/) as the database of choice.
- [ReactJS](https://reactjs.org/) in the front end (with [Blueprint](https://www.blueprintjs.com/) component library).
- [Webpack](https://webpack.js.org/) to bundle most of the front end code.
