# Django Project - RE:BORN WEB



## Description

**Inje Uni. ComputerEngineering Website**

This is a Django framework-based academic homepage project aimed at improving the inconvenience of the existing academic homepage and for smooth communication and communication among undergraduate students.

- **Website Address : http://inje-reborn.com/**
- **Development Record : https://parkhyeonchae.github.io/**



## Technology

- Framework : Django 3.0.2, Bootstraop 3.4
- Language : Python 3.7.4, JavaScript
- Database : SQLite3
- OS : Window10
- IDE : VsCode
- Distribute : CentOS 7.6
- Library : [Summernote](https://summernote.org/), [Waypoints](http://imakewebthings.com/waypoints/)



## Directory Structure

```
Re-Born-Web/
	reborn_web/
		reborn_web/
			settings.py
			urls.py
		users/
		notice/
		free/
		anonymous/
		calender/
		timetable/
		about/
		templates/
		static/
		media/
		manage.py
		secrets.json
		debug.log
		db.sqlite3
	django_env/
	gitignore
	LICENSE
	requirements.txt
```

### reborn_web

In `settings.py`, language code, timezone, templates path, static path, media path setting, etc. are done. Add the created app to installed_app and Match the url.py for each app in the url.py path within this directory.

### users

This is the user account app. We implemented functions such as basic login, membership, authentication using SMTP, profile modification, ID/password finding with Ajax, password change, and membership withdrawal.

### notice

This is the department announcement app. Only accounts with administrator rights can be CRUD, and features such as searching for postings and displaying notices have been added.

### free

It's a free bulletin board app. We added categories such as questions and information, and unlike the notice app, we added functions such as comment and reply with Ajax.

### anonymous

It's an anonymous bulletin board app. This is an infinite scroll-type bulletin board with the motif of Facebook Timeline and Everytime. The author is anonymous and has added features such as recommendation.

### calender

It's a course schedule app. Only accounts with administrator rights can add, delete, and modify schedules, and the schedule was implemented in the D-Day format using query statements on the index page.

### timetable

This is the department test timetable app. You can view the exam schedule in a table format by selecting only the exam schedule by grade and the subjects you take. Users with administrator privileges can update the test schedule and have implemented it to display the last update time.

### about

It is an app that adds functions such as student council information, club in department, and laboratory introduction.

### templates

Do not create template folders for each app, but manage them in this directory.

### static

Manage static files such as css, js, and img of project. You can collect static files with the `collectstatic` command at distribution time.

### media

Path to store media files, such as files and picture attachments.

### manage.py

The standard Django `manage.py`.

### secrets.json

Detach the `secret key` of django here. In addition, you add hidden values, such as the password used by smtp.



## Execution

### Repogitory Clone

```
$ git clone https://github.com/ParkHyeonChae/Re-Born-Web.git
```

### Install PIP

```
$ pip install -r requirements.txt
```

### Running Virtual Environment

```
$ cd django_env
$ cd Scripts
$ activate
```

### Create Media Directory & Secrets File

```
$ cd reborn_web
$ mkdir media
$ type NUL > secrets.json // Window
$ touch secrets.json // Linux
```

### DB Migration

```
$ cd reborn_web
$ python manage.py makemigrations
$ python manage.py migrate
```

### Create Super User

```
$ python manage.py createsuperuser
```

### Runserver

```
$ python manage.py runserver
```



## License

- **MIT License**
- **Copyright (c) 2020 ParkHyeonChae**