from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Profile
from .serializers import RegisterSerializer, ProfileSerializer


# User Registration
class RegisterView(generics.CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


# View Logged-in User Profile
class ProfileView(generics.RetrieveAPIView):

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile