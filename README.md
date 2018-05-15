
# Introduction
This project uses psycopg2 to query a mock PostgreSQL database for a fictional news website. 

The news database contains three tables:
* authors
	* name - text 
	* bio -text 
	* id - integer 
* articles
	* author - integer 
	* title - text 
	* slug - text 
	* lead - text 
	* body - text 
	* time - timestamp with time zone 
	* id - integer 
* log
	* path - text 
	* ip - inet 
	* method - text 
	* status - text 
	* time - timestamp with time zone  
	* id - integer 

The python script "answers.py" answers three questions: 
	1. What are the most popular three articles of all time?
	2. Who are the most popular article authors of all time?
	3. On which days did more than 1% of requests lead to errors?

# Requirements: 
1. Vagrant 
	* https://www.vagrantup.com/downloads.html
2. VirtualBox 
	* https://www.virtualbox.org/

If not relying on vagrant, set up environment with: 
1. Python 2.7 
2. PostgreSQL 
3. psycopg2

# How to create the news database: 
## Setting up the virtual environment: 
1. Download the fsnd-virtual-machine.zip file from the git repository. 
2. Unzip the file and move the folder somewhere easily accessible. 
3. Move the newsdata.sql file from the newsdata.zip file into  ".../FSND-Virtual-Machine/vagrant"
4. Open a terminal ("Git Bash" for Windows or Terminal for Linux/Mac) (after installing Vagrant and VirtualBox)
5. Cd (Change Directory) into FSND-Virtual-Machine/vagrant
6. Type "vagrant up" 
7. Wait for initialization the virtual machine. 
8. Type "vagrant ssh" to log into the virtual machine 

## Creating the database: 
1. After logging into the virtual machine, type "psql -d news -f -newsdata.sql" for the first time you set up the database
2. After setting up the database initially, simply type "psql -d news" to access the database. 


# Required Views 
In order to run the code, you will need to have these views: 

## Option 1: 
Type "psql -d news -f create_views.sql" in the command line interface 
with create_views.sql located in the vagrant folder. 

## Option 2
Run each of these views individually:


1. CREATE VIEW titlecount  
AS SELECT title, COUNT(*) as count 
FROM articles LEFT JOIN log 
ON log.path = concat('/article/', articles.slug) 
GROUP BY title
ORDER BY count
DESC;


> This view sorts through the log table and groups the paths by article slug/title.

		
2. CREATE VIEW authortitlecount 
AS SELECT articles.author, articles.title, count 
FROM titlecount JOIN articles 
ON titlecount.title = articles.title;
> This view holds the author IDs, the title of the article, and the number of times each article was hit.
	
3. CREATE VIEW authoridsum AS 
SELECT authortitlecount.author, SUM(count) 
FROM authortitlecount 
GROUP BY author 
ORDER BY SUM(count) DESC;
> This view holds the author IDs and the sum of the counts of each author IDs articles.
  
4. CREATE VIEW daylogstotal AS 
SELECT date_trunc('day', time) as day, 
count(*) as Total_Logs 
FROM log GROUP BY day;
> This view holds then total number of logs grouped by day.


5. CREATE VIEW daylogs404errors 
AS SELECT time::date AS day, count(*) as error_count FROM log 
WHERE status = '404 NOT FOUND' GROUP BY day;
> This article holds the total number of 404 NOT FOUND errors grouped by day. 
# Running the Script 
To run the script do the following: 
1. SSH into the Vagrant VM
2. CD into the folder containing answers.py 
3. Type "python answers.py" and press enter. 
4. Three tables answering each question should appear on your screen.   