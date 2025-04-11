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
    path("api/", include(router.urls)),
    path("auth/", include("rest_framework.urls"))
]
