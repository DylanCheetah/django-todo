# django-todo
A simple todo list web application implemented with Django.


## Required Software
* Visual Studio Code
* Python 3
* Django
* Django REST Framework
* Bootstrap


## Prerequisites
01. install Visual Studio Code
02. install Python 3
03. install `Django` and `djangorestframework` via pip


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

### Phase 5: Homepage
01. create "django_todo/todo/templates/todo/layout.html"
02. place the following code into the new file:
```html
{% load static %}

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{% static 'todo/css/bootstrap.min.css' %}">
        <script src="{% static 'todo/js/bootstrap.bundle.js' %}"></script>
        {% block scripts %}
        {% endblock %}
    </head>
    <body>
        {% block content %}
        {% endblock %}
    </body>
</html>

```
03. create "django_todo/todo/templates/todo/index.html"
04. place the following code into the new file:
```html
{% extends "todo/layout.html" %}

{% block title %}Todo{% endblock %}

{% block content %}
    <div class="container-fluid">
        Under construction.
    </div>
{% endblock %}
```
05. open "django_todo/todo/views.py"
06. modify the code like this:
```python
from django.shortcuts import render


# View Functions
# ==============
def index(request):
    return render(
        request,
        "todo/index.html",
        {}
    )
```
07. create "django_todo/todo/urls.py"
08. place the following code in the new file:
```python
from django.urls import path

from .views import index


urlpatterns = [
    path("", index, name="todo-index")
]
```
09. open "django_todo/django_todo/urls.py"
10. modify the code like this:
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("todo.urls")),
    path('admin/', admin.site.urls),
]
```
11. execute `python manage.py runserver`
12. visit http://localhost:8000/ in a web browser and you should see the message "Under construction."

### Phase 6: Account Registration
01. create "django_todo/todo/forms.py"
02. place the following code into the new file:
```python
from django import forms


# Form Classes
# ============
class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput({"class": "m-1 form-control"}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput({"class": "m-1 form-control"}))
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput({"class": "m-1 form-control"}))

    def clean_confirm_password(self):
        # Password and confirm password must match
        if self.cleaned_data["password"] != self.cleaned_data["confirm_password"]:
            raise forms.ValidationError("The passwords must match.")
```
03. create "django_todo/todo/templates/todo/register.html"
04. place the following code into the new file:
```html
{% extends "todo/layout.html" %}

{% block title %}Todo - Register{% endblock %}

{% block content %}
    <div class="container-fluid">
        <div class="row justify-content-center">
            <h1 class="col-10 m-2">Register</h1>
        </div>
        <div class="row justify-content-center">
            <form class="col-10 m-2 card text-bg-light" action="" method="post">
                {% csrf_token %}
                <div class="card-body">
                    {{ form }}
                    <input class="m-1 form-control btn btn-primary" type="submit" value="Register">
                </div>
            </form>
        </div>
    </div>
{% endblock %}
```
05. modify "django_todo/todo/views.py" like this:
```python
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegistrationForm


# View Functions
# ==============
def index(request):
    return render(
        request,
        "todo/index.html",
        {}
    )


def register(request):
    form = RegistrationForm()

    # Process submitted form data
    if request.method == "POST":
        # Validate form data
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Create new user account
            user = User.objects.create(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            # Log in and redirect to the homepage
            login(request, user)
            return redirect(reverse("todo-index"))

    return render(
        request,
        "todo/register.html",
        {
            "form": form
        }
    )
```
06. modify "django_todo/todo/urls.py" like this:
```python
from django.urls import path

from .views import index, register


urlpatterns = [
    path("", index, name="todo-index"),
    path("account/register/", register, name="todo-register")
]
```
07. execute `python manage.py runserver`
08. visit http://localhost:8000/account/register/ and you should be able to register a new user account

### Phase 7: User Login
01. add the following code to "django_todo/todo/forms.py":
```python
class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, widget=forms.TextInput({"class": "m-1 form-control"}))
    password = forms.CharField(max_length=128, widget=forms.PasswordInput({"class": "m-1 form-control"}))
```
02. create "django_todo/todo/templates/todo/login.html"
03. place the following code into the new file:
```html
{% extends "todo/layout.html" %}

{% block title %}Todo - Login{% endblock %}

{% block content %}
    <div class="container-fluid">
        <div class="row justify-content-center">
            <h1 class="col-10 m-2">Login</h1>
        </div>
        {% if error %}
            <div class="row justify-content-center">
                <div class="col-10 m-2 alert alert-danger">{{ error }}</div>
            </div>
        {% endif %}
        <div class="row justify-content-center">
            <form class="col-10 m-2 card text-bg-light" action="" method="post">
                {% csrf_token %}
                <div class="card-body">
                    {{ form }}
                    <input class="m-1 form-control btn btn-primary" type="submit" value="Login">
                </div>
            </form>
        </div>
    </div>
{% endblock %}
```
04. modify "django_todo/todo/views.py" like this:
```python
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegistrationForm


# View Functions
# ==============
def index(request):
    return render(
        request,
        "todo/index.html",
        {}
    )


def register(request):
    form = RegistrationForm()

    # Process submitted form data
    if request.method == "POST":
        # Validate form data
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Create new user account
            user = User.objects.create(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            # Log in and redirect to the homepage
            login(request, user)
            return redirect(reverse("todo-index"))

    return render(
        request,
        "todo/register.html",
        {
            "form": form
        }
    )


def login_view(request):
    form = LoginForm()

    # Process submitted form data
    if request.method == "POST":
        # Validate form data
        form = LoginForm(request.POST)

        if form.is_valid():
            # Authenticate the user
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user:
                # Log the user in and redirect
                login(request, user)
                return redirect(reverse("todo-index"))
            
            # Authentication failed
            return render(
                request,
                "todo/login.html",
                {
                    "error": "Invalid user credentials.",
                    "form": form
                }
            )
        
    return render(
        request,
        "todo/login.html",
        {
            "form": form
        }
    )
```
05. modify "django_todo/todo/urls.py" like this:
```python
from django.urls import path

from .views import index, login_view, register


urlpatterns = [
    path("", index, name="todo-index"),
    path("account/register/", register, name="todo-register"),
    path("account/login/", login_view, name="todo-login")
]
```
06. execute `python manage.py runserver`
07. visit http://localhost:8000/account/login/ and you should be able to log in

### Phase 8: Logging Out
01. modify "django_todo/todo/views.py" like this:
```python
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegistrationForm


# View Functions
# ==============
def index(request):
    return render(
        request,
        "todo/index.html",
        {}
    )


def register(request):
    form = RegistrationForm()

    # Process submitted form data
    if request.method == "POST":
        # Validate form data
        form = RegistrationForm(request.POST)

        if form.is_valid():
            # Create new user account
            user = User.objects.create(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            # Log in and redirect to the homepage
            login(request, user)
            return redirect(reverse("todo-index"))

    return render(
        request,
        "todo/register.html",
        {
            "form": form
        }
    )


def login_view(request):
    form = LoginForm()

    # Process submitted form data
    if request.method == "POST":
        # Validate form data
        form = LoginForm(request.POST)

        if form.is_valid():
            # Authenticate the user
            user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"]
            )

            if user:
                # Log the user in and redirect
                login(request, user)
                return redirect(reverse("todo-index"))
            
            # Authentication failed
            return render(
                request,
                "todo/login.html",
                {
                    "error": "Invalid user credentials.",
                    "form": form
                }
            )
        
    return render(
        request,
        "todo/login.html",
        {
            "form": form
        }
    )


def logout_view(request):
    # Log out and redirect
    logout(request)
    return redirect(reverse("todo-index"))
```
02. modify "django_todo/todo/urls.py" like this:
```python
from django.urls import path

from .views import index, login_view, logout_view, register


urlpatterns = [
    path("", index, name="todo-index"),
    path("account/register/", register, name="todo-register"),
    path("account/login/", login_view, name="todo-login"),
    path("account/logout/", logout_view, name="todo-logout")
]
```
03. execute `python manage.py runserver`
04. visit http://localhost:8000/account/logout/ and you should get redirected to the homepage after logging
out

### Phase 9: Protecting Views
01. import the `login_required` decorator from `django.contrib.auth.decorators`
02. apply the `login_required` decorator to each view which should be only accessible when logged in:
```python
from django.contrib.auth.decorators import login_required
...
@login_required(login_url="/account/login/")
def index(request):
    return render(
        request,
        "todo/index.html",
        {}
    )
```

### Phase 10: Todo List Backend
01. add the following to the bottom of your "django_todo/django_todo/settings.py" file:
```python
# Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
	"PAGE_SIZE": 10,
	"DEFAULT_AUTHENTICATION_CLASSES": [
	    "rest_framework.authentication.SessionAuthentication"
	]
}
```
02. add "rest_framework" to your list of installed apps:
```python
INSTALLED_APPS = [
    "todo",
    "rest_framework",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
03. create "django_todo/todo/serializers.py"
04. place the following code into the new file:
```python
from rest_framework import serializers

from .models import Task, TodoList


# Serializer Classes
# ==================
class TodoListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TodoList
        fields = ["url", "id", "name"]


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Task
        fields = ["url", "id", "name", "due_date", "completed"]
```
05. update the imports in "django_todo/todo/views.py" like this:
```python
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .forms import LoginForm, RegistrationForm
from .models import Task, TodoList
from .serializers import TaskSerializer, TodoListSerializer
```
06. add the following classes to "django_todo/todo/views.py":
```python
# Viewset Classes
# ===============
class TodoListViewSet(ModelViewSet):
    serializer_class = TodoListSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self, request):
        return TodoList.objects.filter(owner=request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self, request):
        return Task.objects.filter(owner__owner=request.user)
```
07. modify "django_todo/todo/urls.py" like this:
```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register("tasks", views.TaskViewSet, "task")
router.register("todo-lists", views.TodoListViewSet, "todolist")


urlpatterns = [
    path("", views.index, name="todo-index"),
    path("account/register/", views.register, name="todo-register"),
    path("account/login/", views.login_view, name="todo-login"),
    path("account/logout/", views.logout_view, name="todo-logout"),
    path("api/v1/", include(router.urls)),
    path("auth/", include("rest_framework.urls"))
]
```

### Phase 11: Todo List View
01. create "django_todo/todo/static/todo/js/todo-list.js"
02. place the following content into the new file:
```js
document.addEventListener("DOMContentLoaded", () => {
    // Globals
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    let todoLists = null;

    // Functions
    function loadTodoLists(url) {
        // Show busy indicator
        document.querySelector("#todoListSpinner").classList.remove("d-none");

        // Fetch todo lists from server
        fetch(url, {
                credentials: "same-origin",
                cache: "no-store"
        })
        .then((response) => response.json())
        .then((payload) => {
            // Store payload
            todoLists = payload;

            // Clear previous page of todo lists
            const todoListView = document.querySelector("#todoListView");

            while(todoListView.childElementCount) {
                todoListView.removeChild(todoListView.firstChild);
            }

            // Display todo lists
            todoLists.results.forEach((todoList) => {
                // Create row
                let row = document.createElement("div");
                row.classList.add("row");

                // Create todo list card
                let todoListCard = document.createElement("div");
                todoListCard.classList.add("col", "m-1", "card", "bg-light");
                row.appendChild(todoListCard);

                // Create card body
                let cardBody = document.createElement("div");
                cardBody.classList.add("card-body", "row");
                cardBody.id = `todoList${todoList.id}`;
                todoListCard.appendChild(cardBody);

                let cardTitle = document.createElement("h5");
                cardTitle.classList.add("col-9", "m-1", "card-title");
                cardTitle.id = `todoListTitle${todoList.id}`;
                cardTitle.innerText = todoList.name;
                cardBody.appendChild(cardTitle);

                let cardEditBtn = document.createElement("button");
                cardEditBtn.classList.add("col-1", "m-1", "btn", "btn-warning");
                cardEditBtn.innerText = "Edit";
                cardEditBtn.dataset.id = todoList.id;
                cardEditBtn.addEventListener("click", (evt) => editTodoList(evt.target.dataset.id));
                cardBody.appendChild(cardEditBtn);

                let cardDeleteBtn = document.createElement("button");
                cardDeleteBtn.classList.add("col-1", "m-1", "btn", "btn-danger");
                cardDeleteBtn.innerText = "Delete";
                cardDeleteBtn.dataset.id = todoList.id;
                cardDeleteBtn.addEventListener("click", (evt) => deleteTodoList(evt.target.dataset.id));
                cardBody.appendChild(cardDeleteBtn);

                // Create editable card body
                let cardBody2 = document.createElement("div");
                cardBody2.classList.add("card-body", "row", "d-none");
                cardBody2.id = `editableTodoList${todoList.id}`;
                todoListCard.append(cardBody2);

                let cardTitleInput = document.createElement("input");
                cardTitleInput.classList.add("col-9", "m-1");
                cardTitleInput.id = `todoListTitleInput${todoList.id}`;
                cardTitleInput.type = "text";
                cardTitleInput.value = todoList.name;
                cardBody2.appendChild(cardTitleInput);

                let cardConfirmEditBtn = document.createElement("button");
                cardConfirmEditBtn.classList.add("col-1", "m-1", "btn", "btn-success");
                cardConfirmEditBtn.innerText = "Confirm";
                cardConfirmEditBtn.dataset.id = todoList.id;
                cardConfirmEditBtn.addEventListener("click", (evt) => confirmEditTodoList(evt.target.dataset.id));
                cardBody2.appendChild(cardConfirmEditBtn);

                let cardCancelEditBtn = document.createElement("button");
                cardCancelEditBtn.classList.add("col-1", "m-1", "btn", "btn-danger");
                cardCancelEditBtn.innerText = "Cancel";
                cardCancelEditBtn.dataset.id = todoList.id;
                cardCancelEditBtn.addEventListener("click", (evt) => cancelEditTodoList(evt.target.dataset.id));
                cardBody2.appendChild(cardCancelEditBtn);

                // Add row to todo list view
                todoListView.appendChild(row);
            });

            // Update page turner
            // TODO

            // Hide busy indicator
            document.querySelector("#todoListSpinner").classList.add("d-none");
        })
        .catch((err) => {
            console.error(err);
        });
    }


    function addTodoList() {
        const nameInput = document.querySelector("#todoListNameInput");

        fetch("/api/v1/todo-lists/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                name: nameInput.value
            }),
            credentials: "same-origin",
            cache: "no-store"
        })
        .then((response) => {
            // Check status code
            if(response.status != 201) {
                alert("Failed to add todo list.");
                return;
            }

            // Clear todo list name input
            nameInput.value = "";

            // Reload todo lists
            loadTodoLists("/api/v1/todo-lists/");
        })
        .catch((err) => {
            console.error(err);
        });
    }


    function editTodoList(id) {
        // Hide read-only todo list and show editable todo list
        document.querySelector(`#todoList${id}`).classList.add("d-none");
        document.querySelector(`#editableTodoList${id}`).classList.remove("d-none");
    }

    
    function deleteTodoList(id) {
        fetch(`/api/v1/todo-lists/${id}/`, {
            method: "DELETE",
            headers: {
                "X-CSRFToken": csrfToken
            },
            credentials: "same-origin",
            cache: "no-store"
        })
        .then((response) => {
            // Check status code
            if(response.status != 204) {
                alert("Failed to delete todo list.");
                return;
            }

            // Reload todo lists
            loadTodoLists("/api/v1/todo-lists/");
        })
        .catch((err) => {
            console.error(err);
        });
    }


    function cancelEditTodoList(id) {
        // Sync todo list title input with todo list title
        document.querySelector(`#todoListTitleInput${id}`).value = document.querySelector(`#todoListTitle${id}`).innerText;

        // Hide editable todo list and show read-only todo list
        document.querySelector(`#editableTodoList${id}`).classList.add("d-none");
        document.querySelector(`#todoList${id}`).classList.remove("d-none");
    }


    function confirmEditTodoList(id) {
        console.log(`Confirm edit of todo list ${id}...`);

        // Get new todo list name
        const todoListTitleInput = document.querySelector(`#todoListTitleInput${id}`);

        // Update todo list name
        fetch(`/api/v1/todo-lists/${id}/`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
                name: todoListTitleInput.value
            }),
            credentials: "same-origin",
            cache: "no-store"
        })
        .then((response) => {
            // Check status code
            if(response.status != 200) {
                alert("Failed to update todo list.");
                return;
            }

            // Reload todo lists
            loadTodoLists("/api/v1/todo-lists/");
        })
        .catch((err) => {
            console.error(err);
        });
    }


    function previousPage() {
        if(!todoLists.previous) {
            return;
        }

        loadTodoLists(todoLists.previous);
    }


    function nextPage() {
        if(!todoLists.next) {
            return;
        }
        
        loadTodoLists(todoLists.next);
    }

    // Add event listeners
    const addTodoListBtn = document.querySelector("#addTodoList");
    const prevPageBtn = document.querySelector("#prevPageBtn");
    const nextPageBtn = document.querySelector("#nextPageBtn");

    addTodoListBtn.addEventListener("click", addTodoList);
    prevPageBtn.addEventListener("click", previousPage);
    nextPageBtn.addEventListener("click", nextPage);

    // Load first page of todo lists
    loadTodoLists("/api/v1/todo-lists/");
});
```
02. modify "django_todo/todo/templates/todo/layout.html" like this:
```html
{% load static %}

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>{% block title %}{% endblock %}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="stylesheet" href="{% static 'todo/css/bootstrap.min.css' %}">
        <script src="{% static 'todo/js/bootstrap.bundle.js' %}"></script>
        {% block scripts %}
        {% endblock %}
    </head>
    <body>
        {% block content %}
        {% endblock %}
    </body>
</html>
```
03. modify "django_todo/todo/templates/todo/index.html" like this:
```html
{% extends "todo/layout.html" %}
{% load static %}

{% block title %}Todo{% endblock %}

{% block scripts %}
    <script src="{% static 'todo/js/todo-list.js' %}"></script>
{% endblock %}

{% block content %}
    {% csrf_token %}
    <div class="container-fluid">
        <div class="row justify-content-center">
            <div class="col-10 m-2 card">
                <div class="card-body">
                    <h1 class="card-title">Todo Lists</h1>
                    <div class="row justify-content-center">
                        <input class="col-10 m-1" id="todoListNameInput" type="text" placeholder="New Todo List">
                        <button class="col-1 m-1 btn btn-primary" id="addTodoList">Add</button>
                    </div>
                    <div id="todoListView"></div>
                    <div class="row justify-content-center">
                        <div class="spinner-border" id="todoListSpinner">
                            <div class="visually-hidden">Loading...</div>
                        </div>
                    </div>
                    <nav class="row justify-content-center">
                        <ul class="col-2 m-1 pagination">
                            <li class="page-item"><a class="page-link" id="prevPageBtn" href="#">Previous</a></li>
                            <li class="page-item"><a class="page-link" id="nextPageBtn" href="#">Next</a></li>
                        </ul>
                    </nav>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
```

### Phase 12: Task View
TODO
