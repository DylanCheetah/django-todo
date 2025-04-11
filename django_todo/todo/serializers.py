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
