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
