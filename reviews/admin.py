"""Admin configuration for the reviews app.

Registers the `Review` model and exposes filters and search fields
that are useful when moderating or inspecting feedback.
"""

from django.contrib import admin

from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    """Admin for `Review` with common list and filter settings."""

    list_display = ("id", "business_user", "reviewer", "rating", "updated_at")
    list_filter = ("rating", "business_user")
    search_fields = ("business_user__username", "reviewer__username", "description")
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Review, ReviewAdmin)
