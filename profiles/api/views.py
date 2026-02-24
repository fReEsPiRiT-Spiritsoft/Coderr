from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from profiles.models import Profile
from .serializers import ProfileSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

class ProfileDetailAPIView(RetrieveUpdateAPIView):
    """
    GET  /api/profile/{pk}/   -> any authenticated user
    PATCH /api/profile/{pk}/  -> only profile owner
    """
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'pk'


class ProfileListByTypeAPIView(ListAPIView):
    """
    Base list view for profiles filtered by type ('business' or 'customer').
    Authenticated users only.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    lookup_type = None

    def get_queryset(self):
        t = getattr(self, 'lookup_type', None)
        qs = Profile.objects.select_related('user').all()
        if t:
            qs = qs.filter(type=t)
        return qs.order_by('user_id')

class BusinessProfilesAPIView(ProfileListByTypeAPIView):
    lookup_type = 'business'

class CustomerProfilesAPIView(ProfileListByTypeAPIView):
    lookup_type = 'customer'