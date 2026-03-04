"""Admin configuration for the orders app.

Registers `Order` with a compact `ModelAdmin` that exposes status,
participants and timestamps for quick inspection in the admin.
"""

from django.contrib import admin

from .models import Order


class OrderAdmin(admin.ModelAdmin):
    """Basic admin settings for `Order` objects."""

    list_display = (
        "id",
        "title",
        "customer_user",
        "business_user",
        "price",
        "status",
        "created_at",
    )
    list_filter = ("status", "offer_type", "business_user", "customer_user")
    search_fields = ("title", "customer_user__username", "business_user__username")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"


admin.site.register(Order, OrderAdmin)
