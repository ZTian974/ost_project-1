ost_project
---
####[blog URL](http://ec2-54-200-28-13.us-west-2.compute.amazonaws.com/blog/)
This blog system is built by Django, Apache, MySQL and Bootstrap, and is deployed on EC2 of AWS. The system handles multiple users and each user is able to create one or more blogs. A user can select a blog that he owns and write posts to it.

Posts are sorted by modification time and orginated no more than 5 pages each page. Every page has 'next' and 'previous' links to other pages.

Install
---
* development environment on ubuntu
	
	a. update system
	command: sudo apt-get update

	b. install LAMP package (ref: https://help.ubuntu.com/community/ApacheMySQLPHP)
		install tasksel: sudo apt-get install tasksel
		
		install LAMP: sudo tasksel install lamp-server
		need set up mysql account in this step

		optional install pypmyadmin: sudo apt-get install phpmyadmin

	c. install mod_wsgi (ref: https://www.digitalocean.com/community/articles/installing-mod_wsgi-on-ubuntu-12-04)
		sudo aptitude install apache2 apache2.2-common apache2-mpm-prefork apache2-utils libexpat1 ssl-cert

		sudo aptitude install libapache2-mod-wsgi

		sudo service apache2 restart

	d. install python-mysqldb
		sudo apt-get install python-mysqldb

	e. install django
		install optional package:
			sudo aptitude install python-imaging python-pythonmagick python-markdown python-textile python-docutils

		use pip install django:
			install pip and virtualenv (ref: http://www.saltycrane.com/blog/2010/02/how-install-pip-ubuntu/)
				sudo apt-get install python-pip python-dev build-essential

				sudo pip install --upgrade pip

				sudo pip install --upgrade virtualenv

			install django:
				sudo pip install Django


2. create a database named "xxx" in mysql

3. config database in ost_project/setting.py, and change the DATABASES' 'NAME' entry as the name "xxx"

4. get the project main directory "ost_project", 
	command: python manage.py sql blog
if there is no error, your database setting is right
	command: python manage.py syncdb
you might a admin user in this step, if it's your first time to run this app

5. run this app
 	command: python manage.py runserver
 go to http://127.0.0.1:8000/blog/ or http://127.0.0.1:8000/admin
