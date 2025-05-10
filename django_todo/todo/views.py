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


# Viewset Classes
# ===============
class TodoListViewSet(ModelViewSet):
    serializer_class = TodoListSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return TodoList.objects.filter(owner=self.request.user).order_by("name")
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    

class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return Task.objects.filter(owner__owner=self.request.user).order_by("name")


# View Functions
# ==============
@login_required(login_url="/account/login/")
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
