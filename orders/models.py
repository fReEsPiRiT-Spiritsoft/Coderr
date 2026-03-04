"""Order model.

Represents an order created by a customer for an offer detail. The
model includes references to both the customer and the business user,
order metadata (price, delivery time, features) and a status field to
track progress.
"""

from django.contrib.auth.models import User
from django.db import models


class Order(models.Model):
    """A customer order for a specific offer tier.

    The model stores both participants (`customer_user` and
    `business_user`), a copy of the chosen offer detail metadata and a
    `status` field used to track the order lifecycle.
    """

    STATUS_CHOICES = (
        ("pending", "pending"),
        ("in_progress", "in_progress"),
        ("completed", "completed"),
        ("cancelled", "cancelled"),
    )

    OFFER_TYPE_CHOICES = (("basic", "basic"), ("standard", "standard"), ("premium", "premium"))

    customer_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="customer_orders")
    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="business_orders")
    title = models.CharField(max_length=255)
    revisions = models.IntegerField(default=0)
    delivery_time_in_days = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    features = models.JSONField(blank=True, default=list)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPE_CHOICES, default="basic")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.id} - {self.title}"