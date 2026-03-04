"""URL routes for the authentication API.

Defines two endpoints: registration and login which are implemented in
``authentication.api.views``.
"""

from django.urls import path

from .views import login_view, registration

urlpatterns = [
    path("registration/", registration, name="api-registration"),
    path("login/", login_view, name="api-login"),
]