"""API views for authentication endpoints.

Provides two simple JSON endpoints for registration and login that
return an authentication token on success. The views are small and
intended to be used by the frontend during user onboarding and sign-in.
"""

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import LoginSerializer, RegistrationSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def registration(request):
    """Register a new user and return an auth token.

    Expects the same input fields as :class:`RegistrationSerializer`.
    On success returns a JSON object containing a token and basic
    user information.
    """

    serializer = RegistrationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as exc:  
        return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """Authenticate a user and return an auth token.

    Uses :class:`LoginSerializer` to validate credentials. On success
    returns the auth token and basic user information.
    """

    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_id": user.id,
            },
            status=status.HTTP_200_OK,
        )
    except Exception as exc:  
        return Response({"detail": "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)