from django.db import models
from django.contrib.auth.models import User

class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='offers/', blank=True, null=True)
    description = models.TextField(blank=True, default='')
    min_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    min_delivery_time = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'Offer {self.id} - {self.title}'


class OfferDetail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='details')
    url = models.URLField(max_length=1024)

    def __str__(self):
        return f'OfferDetail {self.id} for Offer {self.offer_id}'