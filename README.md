# CS50-Final-Project
In this project I tried to put into practice much of what I learned in the course, I took some examples to carry out my tasks in the creation of this CRUD.

## Installation Instructions

### Cloning the Repo

```
mkdir finalProjectMC
cd finalProjectMC
git clone https://github.com/MaurSc/contactbook.git
cd contactbook
```
### Prerequsites

Make sure you have Python3 installed and __you use it to run this program.__

Furthermore, you have to make sure you have Flask installed. If not you can use pip or your favourite package manager to install it.

```
pip3 install flask 
```

The following Packages should be preinstalled but if something is missing make sure these are also ready to use:

* cs50
* flask_session
* Random
* Datetime
* Json
* Urllib3
* Urllib

### Setup

First you have to set the FLASK_APP environment variable.

Standard Way
```
export FLASK_APP=application.py
export FLASK_ENV=development
```

For Powershell
```
$env:FLASK_APP="application.py"
$env:FLASK_ENV="development"
```


### Running it

To execute the program run the following
```
flask run
```

## Contenido de ContactBook folder:

### ContactBook:

        When entering the directory of our project we can see that we have 3 files
    1. Application:
        -This file contains the main and necessary functions to be able to give the necessary dynamism to our entire project.
        In the header are the necessary libraries for the realization of the project, among which are those of CS50 - SQL
        also some functions to has passwords, to verify the login, etc,
        use what you have learned in the course to serve the application with data from a sqlite DB.
        After that I define the functions that will be triggered with the browser's response.
    2. Helpers:
        -Here I define the function of the need for the user to be logged into the system in order to continue performing actions within it,
        redirecting it to the login tab whenever it tries to perform an action without being inside the system.
    3. Phonebook:
        -Database which the whole system uses, it contains two different tables linked to each other.
        These verify that the contacts correspond to the user who is currently logged into the system.

### Static:

        This folder contains everything related to the visualization of the application, it would be the part of ** V ** in the ** MVC ** model.
    This folder only contains the CSS file.

### Templates:

        This folder contains in its interior what refers to the structure of the entire application, it is done using JINJA2.
    1. Register:
        - This template is used to allow the user to create an account within the application to later be able to serve,
        with your data to it.
    2. Login:
        - Allows the user to enter with their associated account to add, view, update or delete contacts from their agenda.
    3. Index:
        -After the user creates a valid account, and enters the system on the page, he will be able to view all his contacts.
    4. Logout:
        -From here the user will be able to log out of their account to prevent any intruder with access to their device from having inadvertent access to their contacts.
    5. Add:
        -Here the user will be able to introduce new contacts that for organizational reasons cannot share a name, that is, it must be unique.
    6. Edit:
        -The user has complete freedom to edit the number and email of their contact.
    7. Delete:
        -From here the user will be able to eliminate the users that he wishes convenient.
        
## Video Demo:  
https://youtu.be/w3sp3H2M9E4
