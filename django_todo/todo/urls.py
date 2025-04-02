from django.urls import path

from .views import index, register


urlpatterns = [
    path("", index, name="todo-index"),
    path("account/register/", register, name="todo-register")
]
