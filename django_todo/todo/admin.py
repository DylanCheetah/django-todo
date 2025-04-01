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
