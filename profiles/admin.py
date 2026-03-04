"""Admin configuration for the profiles app.

Registers `Profile` and exposes basic filters and search fields.
The configuration is intentionally small and can be extended when
additional profile fields or relationships are added.
"""

from django.contrib import admin

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    """Minimal admin settings for `Profile` objects."""

    list_display = ("id", "user", "type", "location", "tel", "updated_at")
    list_filter = ("type",)
    search_fields = ("user__username", "location", "tel")
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Profile, ProfileAdmin)
