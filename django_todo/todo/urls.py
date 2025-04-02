from django.urls import path

from .views import index, login_view, register


urlpatterns = [
    path("", index, name="todo-index"),
    path("account/register/", register, name="todo-register"),
    path("account/login/", login_view, name="todo-login")
]
