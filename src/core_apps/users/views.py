from .serializers import UserSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model


class CustomUserDetailsView(RetrieveUpdateAPIView):
    """Detail view using custom user model"""

    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Returns the requested user"""
        return self.request.user

    def get_queryset(self):
        """Returns user model instance"""
        return get_user_model().objects.none()
