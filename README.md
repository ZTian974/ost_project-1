ost_project
---
####[blog System URL](http://ec2-54-200-28-13.us-west-2.compute.amazonaws.com/blog/)
This blog system is built by Django, Apache, MySQL and Bootstrap, and is deployed on EC2 of AWS. 

* **multiple users** - The system handles multiple users and each user is able to create one or more blogs. A user can select a blog that he owns and write posts to it.
* **tags** - each post has any number of tags and click a tag can view all posts marked by that tag. 
* **pagenation** - every page has 'next' and 'previous' links to other pages, and each page has no more than 5 posts. 
* **uploads** - user can upload images or other kind of files.
* **RSS** - each blog has RSS link, that dumps a entire blog in XML format.
* **embedded URL** 

Install
---
##### development environment on ubuntu
	
* update system: `sudo apt-get update`

* install LAMP package ([ref](https://help.ubuntu.com/community/ApacheMySQLPHP))
	- install tasksel: `sudo apt-get install tasksel`
		
	- install LAMP: `sudo tasksel install lamp-server`. need set up mysql account in this step

	- optional install pypmyadmin: `sudo apt-get install phpmyadmin`

* install mod_wsgi ([ref](https://www.digitalocean.com/community/articles/installing-mod_wsgi-on-ubuntu-12-04))
	

	   `sudo aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert`

	   `sudo aptitude install libapache2-mod-wsgi`

	   `sudo service apache2 restart`


* install python-mysqldb: `sudo apt-get install python-mysqldb`

* install django
	- install optional package: `sudo aptitude install python-imaging python-pythonmagick python-markdown python-textile python-docutils`
	- use pip install django:
		install pip and virtualenv ([ref](http://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/))
			
		`sudo apt-get install python-pip python-dev build-essential`

		`sudo pip install --upgrade pip`

		`sudo pip install --upgrade virtualenv`

	- install django: `sudo pip install Django`

config
---
* create a database named "xxx" in mysql

* config database in ost_project/setting.py, and change the DATABASES' 'NAME' entry as the name "xxx"

* get the project main directory "ost_project", input command: `python manage.py sql blog`. If there is no error, your database setting is right.

* create tables in database: `python manage.py syncdb`. You can set a admin user in this step, if it's your first time to run this app.

* run this app: `python manage.py runserver`. Visit `http://127.0.0.1:8000/blog/` or `http://127.0.0.1:8000/admin`
