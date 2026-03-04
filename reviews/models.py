from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    business_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_reviews'
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='written_reviews'
    )
    rating = models.IntegerField(default=5)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'Review {self.id} - {self.business_user.username} by {self.reviewer.username}'