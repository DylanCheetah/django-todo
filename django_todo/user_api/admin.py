from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import ngettext

from .models import Ban
from . import utils


# Model Admin Classes
# ===================
# We need to unregister the default user model admin first
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    actions = ["ban", "unban"]

    @admin.action(description="Ban selected users")
    def ban(self, request, queryset):
        # Ban all selected users
        for user in queryset:
            utils.ban_user(user)

        # Show success message
        user_count = len(queryset)
        self.message_user(
            request,
            ngettext(
                "%d user was successfully banned",
                "%d users were successfully banned",
                user_count
            )
            % user_count,
            messages.SUCCESS
        )

    @admin.action(description="Unban selected users")
    def unban(self, request, queryset):
        # Unban all selected users
        for user in queryset:
            utils.unban_user(user)

        # Show success message
        user_count = len(queryset)
        self.message_user(
            request,
            ngettext(
                "%d user was successfully unbanned",
                "%d users were successfully unbanned",
                user_count
            )
            % user_count,
            messages.SUCCESS
        )


@admin.register(Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ["user"]
    readonly_fields = ["user"]
    search_fields = ["user__username"]
