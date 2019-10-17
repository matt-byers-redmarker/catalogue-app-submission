# Udacity Project: Catalogue Application

This project contains code for a locally hosted catalogue application, which displays a catalogue of items within different categories of sports. The aim of this project is to produce a locally hosted web application which allows a user to login with Google Oauth and view content from a database, as well as create, edit, read and delete content on the app. The users' aility to create items is contingent on being logged into the app, and their ability to edit and delete an item is contingent on that user being the initial creator of the item. The app also has JSON endpoints for accessing data in the database. 
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which day/s did more than 1% of requests lead to errors?

## Requirements for running the script

This script is run through a Linux-based virtual machine. For this project, you must have Vagrant and Virtualbox set up on your machine. This script also uses python 3.7.4, so python 3 must be installed. To install all of these, follow the instructions in the links below:

* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Virtualbox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* [Python 3](https://www.python.org/downloads/)

This project also requires the python modules: Flask, SQLAlchemy, itsdangerous, and google-oauth. To download these follow the instructions below in 'How to run the script'. 
All of the requirements for the visual styling are reliant on the Bulma CSS framework which is included in the project. All the requirements for Google Oauth login are also included in the project already. 

## Contents required to run this project
* database_setup.py > script for setting up the database
* catalogue_application.py > script required for running the application continuously
* database_setup.py > script for populating the database with dummy data to be displayed in the app
* 'templates' directory with the following files:
    * catalogue.html
    * category.html
    * deleteItem.html
    * editItem.html
    * head.html
    * header.html
    * item_restricted.html
    * item.html
    * login.html
    * newitem.html
* 'static' directory, with a 'css' disrectory inside with the file: main.css > this controls the page styling and css
* README.md > this file, explains the project and running requirements
_The following files which are not included in this repository are also required to run this script_
* Vagrantfile > this file should be included in the root 'vagrant' folder you downloaded when installing Vagrant

## How to run the script

1. Download and install Vagrant and Virtualbox
2. Open a terminal, git bash, or other command line tool.
3. cd into your directory containing the 'vagrant' folder installed after downloading vagrant.
4. Launch the virtual machine with `vagrant up`
5. Finalise launch of the virtual machine with `vagrant ssh`
6. This will start a new command line instance in your virtual machine. While in here cd into your /vagrant folder.
7. To download python3 and pip package manager, run the bash command `sudo apt-get install python3 python3-pip`. Check you have python3 installed with the command `python3 -V`.
8. Install flask using pip with the bash command `pip3 install Flask`
9. Install SQLAlchemy using pip with the bash commmand `pip3 install SQLAlchemy`
10. Install itsdangerous password manager using pip with the bash commmand `pip3 install itsdangerous`
11. Install google-oauth package using pip with the bash commmand `pip3 install google-oauth`
12. **If you get a permission error installing any of the above packages, preface the command with 'sudo', e.g:** `sudo pip3 install Flask'
9. Download this repository with the bash command `git clone https://github.com/matt-byers-redmarker/catalogue-app-submission.git`
10. Once downloaded, cd into the /catalog folder
11. Once inside the project folder, setup the database by running the bash command `python3 database_setup.py`. You will know that the database has been initialised correctly when the file MBitemCatalog.db is created in the root directory.
12. Once the database has been set up, create the dummy data by running the bash command `python3 lots_of_categories.py`
13. Once the dummy data has been created, run the application on localhost port 8000 by running the bash command `python3 catalogue_application.py`
14. View the application online by navigating to `http://localhost:8000/`

