from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from profiles.models import Profile
from .serializers import ProfileSerializer
from .permissions import IsOwnerOrReadOnly

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
