from django.contrib import admin
from .models import Meeting, ActionItem


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "date", "owner")
    list_filter = ("date", "owner")
    search_fields = ("title", "owner")


@admin.register(ActionItem)
class ActionItemAdmin(admin.ModelAdmin):
    list_display = ("id", "meeting", "owner", "due_date", "status")
    list_filter = ("status",)
    actions = ["mark_completed"]

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True

        return obj.owner == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return True
        return obj.owner == request.user or request.user.is_superuser

    def mark_completed(self, request, queryset):
        queryset.update(status="completed")
    mark_completed.short_description = "Mark selected tasks as completed"

