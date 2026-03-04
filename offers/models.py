"""Offer models.

The module defines `Offer` and `OfferDetail` which represent a user's
service listing and the specific package tiers that belong to an
offer. Fields are intentionally simple and store prices, delivery
times and a JSON list of `features` per detail tier.
"""

from django.contrib.auth.models import User
from django.db import models


class Offer(models.Model):
    """A top-level offer/listing created by a business user.

    - `user`: owner of the offer
    - `title`, `description`: textual metadata
    - `image`: optional representative image stored under `offers/`
    - `min_price`, `min_delivery_time`: convenience fields summarising the
      cheapest/fastest available detail tier
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="offers")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="offers/", blank=True, null=True)
    description = models.TextField(blank=True, default="")
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_delivery_time = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Offer {self.id} - {self.title}"


class OfferDetail(models.Model):
    """A package/tier for an `Offer`.

    Each `OfferDetail` describes a specific tier (basic/standard/premium)
    and contains price, delivery time and a list of features. The
    `offer` ForeignKey links the detail back to its parent `Offer`.
    """

    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(blank=True, default=list)
    offer_type = models.CharField(
        max_length=20,
        choices=(("basic", "basic"), ("standard", "standard"), ("premium", "premium")),
        default="basic",
    )

    def __str__(self):
        return f"OfferDetail {self.id} - {self.title}"