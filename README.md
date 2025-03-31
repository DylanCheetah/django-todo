# django-todo
A simple todo list web application implemented with Django.


## Required Software
* Visual Studio Code
* Python 3
* Django
* Bootstrap


## Tutorial
### Phase 1: Project Setup
01. create a project folder
02. open a terminal to the project folder
03. execute `django-admin startproject django_todo` to create a new Django project
04. switch to the "django_todo" folder
05. execute `python manage.py startapp todo` to create the todo app
06. open "django_todo/django_todo/settings.py"
07. add "todo" to the top of the `INSTALLED_APPS` list:
```python
INSTALLED_APPS = [
    "todo",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
