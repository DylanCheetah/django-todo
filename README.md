# django-todo
A simple todo list web application implemented with Django.


## Required Software
* Visual Studio Code
* Python 3
* Django
* Bootstrap


## Prerequisites
01. install Visual Studio Code
02. install Python 3
03. install Django via pip


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

### Phase 2: Data Models
01. open "django_todo/todo/models.py"
02. modify the code like this:
```python
from django.contrib.auth.models import User
from django.db import models


# Data Models
# ===========
class TodoList(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todo_lists")
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name} ({self.owner})"


class Task(models.Model):
    owner = models.ForeignKey(TodoList, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=128)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name
```
03. execute `python manage.py makemigrations` to create migrations for the new data models
04. execute `python manage.py migrate` to apply all migrations

### Phase 3: Admin Site
01. open "django_todo/todo/admin.py"
02. modify the code like this:
```python
from django.contrib import admin, messages
from django.utils.translation import ngettext

from .models import Task, TodoList


# Model Admin Classes
# ===================
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "owner__name", "owner__owner", "due_date"]
    search_fields = ["name", "owner__name", "owner__owner__username"]
    actions = ["mark_complete", "mark_incomplete"]

    @admin.action(description="Mark as complete")
    def mark_complete(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(
            request,
            ngettext(
                "%d task was marked as complete.",
                "%d tasks were marked as complete.",
                updated
            ) % updated,
            messages.SUCCESS
        )

    @admin.action(description="Mark as incomplete")
    def mark_incomplete(self, request, queryset):
        updated = queryset.update(completed=False)
        self.message_user(
            request,
            ngettext(
                "%d task was marked as incomplete.",
                "%d tasks were marked as incomplete.",
                updated
            ) % updated,
            messages.SUCCESS
        )


class TodoListAdmin(admin.ModelAdmin):
    list_display = ["name", "owner"]
    search_fields = ["name"]


# Register data models
admin.site.register(Task, TaskAdmin)
admin.site.register(TodoList, TodoListAdmin)
```
03. execute `python manage.py createsuperuser` and follow the prompts to create a new superuser
04. execute `python manage.py runserver` to start the development server
05. visit http://localhost:8000/admin/ in a web browser
06. login using the same credentials you used to create the superuser
07. you should be able to view, create, edit, and delete registered data models

### Phase 4: Install Bootstrap
01. create "django_todo/todo/static/todo/css/"
02. copy "bootstrap.min.css" to the new folder
02. create "django_todo/todo/static/todo/js/"
03. copy "bootstrap.bundle.js" to the new folder
