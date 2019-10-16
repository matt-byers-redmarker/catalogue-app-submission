# Udacity Project: Logs Analysis

The aim of this project is to produce a python script which queries a database of news data to answer three key reporting questions: 
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which day/s did more than 1% of requests lead to errors?

## Requirements for running the script

This script is run through a Linux-based virtual machine. For this project, you must have Vagrant and Virtualbox set up on your machine. This script also uses python 3.7.4, so python 3 must be installed. To install all of these, follow the instructions in the links below:

* [Vagrant](https://www.vagrantup.com/downloads.html)
* [Virtualbox](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* [Python 3](https://www.python.org/downloads/)

## Contents required to run this project
* news_report.py > script for querying the database
* news_report_example_output.txt > example output of news_report.py
* README.md > this file, explains the project and running requirements
_The following files which are not included in this repository are also required to run this script_
* newsdata.sql > sql file for creating the tables which the news_report.py script queries
* Vagrantfile > this file should be included in the 'vagrant' folder you download when installing Vagrant

## How to run the script

1. Download and install Vagrant, Virtualbox and Python 3.
2. Download this repository and ensure it has each file mentioned above.
3. Open a terminal, git bash, or other command line tool.
4. cd into your directory containing the 'vagrant' folder installed after downloading vagrant.
5. Launch the virtual machine with `vagrant up`
6. Finalise launch of the virtual machine with `vagrant ssh`
7. This will start a new command line instance in your virtual machine. While in here cd into your /vagrant folder.
8. Move the contents of this repository into your vagrant folder.
9. Load the database with `psql -d news -f newsdata.sql`
10. Connect to the database with `\c news`
11. Run the script with `python news_report.py` to query the databse. You should see the output of the script in your terminal.

## Example code output

```
Q: What are the most popular three articles of all time?

Candidate is jerk, alleges rival — 338647 views
Bears love berries, alleges bear — 253801 views
Bad things gone, say good people — 170098 views

Q: Who are the most popular article authors of all time?

Ursula La Multa — 507594 views
Rudolf von Treppenwitz — 423457 views
Anonymous Contributor — 170098 views
Markoff Chaney — 84557 views

Q: On which day/s did more than 1% of requests lead to errors?
```

July 17, — 2.3 errors

## Views:

This view 'daily_error_rate' was used in the query which answered question 3. It creates a table of each day, the total errors, total requests, and the rate of errors relative to total requests.

```
create view daily_error_rate as 
select 
time::date as date,
sum(case when status = '404 NOT FOUND' then 1 else 0 end) as errors,
count(*) as total_requests,
round(100.0*(sum(case when status = '404 NOT FOUND' then 1 else 0 end))/(count(*)), 1) as rate
from log
group by date
order by rate desc;
```
