# Introduction

The goal of this project was to build a simple chat application, to incorporate different django concepts.

Template is written with django 5.2.8 and python 3 in mind.

![Default Main Menu View](__screenshots/main_menu.png?raw=true "Main Menu")
![Default Public Room List View](__screenshots/room_list.png?raw=true "Public Room List")
![Default Public Chat View](__screenshots/chat_room.png?raw=true "Public Chat Room")


### Main features

* Custom User model which is used for authentication and verification throughout the project

* Models to handle public/private chat room as well as messages

* Use of Django templates and template language to visualize the application

* Implementation of static files into the project

* Generation of room IDs for both public and private rooms for use in URL and direct room access

* PostgreSQL as default database

* Extensive testing to verify correct functionality and security

# Usage

To use this template to start your own project:

### Setup virtual enviroment

To setup the project it is advised to create a vurtual enviroment beforehand

    $ python3 -m venv env
    
Then activate the enviroment by using the following command:

Windows:

    $ env/Scripts/activate 

Linux:

    $ source env/bin/activate 

Now use the requirements.txt file to install all the needed packages into the enviroment

    $ pip install -r requirements.txt

To deactivate the virtual enviroment use

    $ deactivate
      
### Setting up PostgreSQL

There needs to be local instance of PostgreSQl running

For the download link and more info visit: https://www.postgresql.org/

Once the local instance is running, go into the config/settings.py file and and change the data connection data under DATABASES to connect to a local PostgreSQL database.

Run the command

    $ python manage.py migrate

to setup four database for the project

### Start the project

To start the project use

    $ python manage.py runserver

Follow the link given in the response to interact with the app in your browser.

# Django Chat App

# Getting Started

On the home screen click "Sign Up" in the top right to register an Account.

Back on the home screen click "Log In" to sign into the account.

From here you can tinker around with the app.

