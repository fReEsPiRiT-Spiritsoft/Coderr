"""Views for profile endpoints.

Provides a retrieve/update view for a single profile and list views to
fetch profiles by their declared `type` (business or customer).
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from profiles.models import Profile

from .permissions import IsOwnerOrReadOnly
from .serializers import ProfileSerializer


class ProfileDetailAPIView(RetrieveUpdateAPIView):
    """GET/PATCH for a single profile.

    - GET: any authenticated user may retrieve the profile
    - PATCH: only the profile owner may update
    """

    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "pk"


class ProfileListByTypeAPIView(ListAPIView):
    """Base list view for profiles filtered by `type`.

    Subclasses set `lookup_type` to either 'business' or 'customer'.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    lookup_type = None

    def get_queryset(self):
        t = getattr(self, "lookup_type", None)
        qs = Profile.objects.select_related("user").all()
        if t:
            qs = qs.filter(type=t)
        return qs.order_by("user_id")


class BusinessProfilesAPIView(ProfileListByTypeAPIView):
    """List all business profiles."""

    lookup_type = "business"


class CustomerProfilesAPIView(ProfileListByTypeAPIView):
    """List all customer profiles."""

    lookup_type = "customer"