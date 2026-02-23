from django.urls import path
from .views import registration, login_view

urlpatterns = [
    path('registration/', registration, name='api-registration'),
    path('login/', login_view, name='api-login'),
]