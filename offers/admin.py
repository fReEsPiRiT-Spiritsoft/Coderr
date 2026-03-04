"""Admin configuration for the offers app.

Provides simple `ModelAdmin` classes and an inline to manage
`Offer` and `OfferDetail` from the Django admin.

This file keeps admin configuration minimal but useful for
development and debugging (list displays, search and filters).
"""

from django.contrib import admin

from .models import Offer, OfferDetail


class OfferDetailInline(admin.TabularInline):
    """Inline configuration for `OfferDetail` shown on `Offer` pages."""

    model = OfferDetail
    extra = 0
    fields = (
        "title",
        "offer_type",
        "price",
        "delivery_time_in_days",
        "revisions",
    )
    show_change_link = True


class OfferAdmin(admin.ModelAdmin):
    """Admin for `Offer` with useful list and search options."""

    list_display = (
        "id",
        "title",
        "user",
        "min_price",
        "min_delivery_time",
        "updated_at",
    )
    list_filter = ("user",)
    search_fields = ("title", "description", "user__username")
    inlines = (OfferDetailInline,)
    ordering = ("-updated_at",)
    date_hierarchy = "updated_at"


admin.site.register(Offer, OfferAdmin)
admin.site.register(OfferDetail)
