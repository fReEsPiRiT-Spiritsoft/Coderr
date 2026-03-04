"""Review model.

Represents a review left by a customer for a business user. Stores a
rating and optional description as well as timestamps.
"""

from django.contrib.auth.models import User
from django.db import models


class Review(models.Model):
    """A review left for a business by a reviewer."""

    business_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="written_reviews")
    rating = models.IntegerField(default=5)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Review {self.id} - {self.business_user.username} by {self.reviewer.username}"