"""Profile Views that provide profile specific apiviews."""
# TODO: change this in production
from authors_api.settings.local import DEFAULT_FROM_EMAIL
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from .exceptions import CantFollowYourself
from .models import Profile
from .pagination import ProfilePagination
from .renderers import ProfileJSONRenderer, ProfilesJSONRenderer
from .serializers import ProfileSerializer, FollowingSerializer, UpdateProfileSerializer

User = get_user_model


class ProfileListAPIView(generics.ListAPIView):
    """A list view that returns all profiles."""

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    pagination_class = ProfilePagination
    renderer_classes = (ProfilesJSONRenderer,)


class ProfileDetailAPIView(generics.RetrieveAPIView):
    """A detailed view of a single user profile"""

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    renderer_classes = [ProfileJSONRenderer]

    def get_queryset(self):
        """Returns a queryset of all user objects"""
        queryset = Profile.objects.select_related("user")
        return queryset

    def get_object(self):
        """Returns the request users profile"""
        user = self.request.user
        profile = self.get_queryset().get(user=user)
        return profile


class UpdateProfileAPIView(generics.RetrieveAPIView):
    """A view for updating user profile."""

    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    renderer_classes = [ProfileJSONRenderer]

    def get_object(self):
        """Returns the requests user profile"""
        profile = self.request.user.profile
        return profile

    def patch(self, request, *args, **kwargs):
        """Patches the data in UpdateProfileSerializer and returns 200 status if valid. Otherwise raises exception."""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class FollowerListView(APIView):
    """A list view for showing followers"""

    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        """Gets the request user id and returns followers_count, followers, and status_code. If profile does not exist returns 404."""
        try:
            profile = Profile.objects.get(user__id=request.user.id)
            follower_profiles = profile.followers.all()
            serializer = FollowingSerializer(follower_profiles, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "followers_count": follower_profiles.count(),
                "followers": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=404)


class FollowingListView(APIView):
    """A list view showing who the request user is following."""

    def get(self, request, user_id, format=None):
        """Gets the who the user_id is following and returns the status_code, following_count, and users their following. If Profile does not exist returns 404"""
        try:
            profile = Profile.objects.get(user__id=user_id)
            following_profiles = profile.following.all()
            users = [p.user for p in following_profiles]
            serializer = FollowingSerializer(users, many=True)
            formatted_response = {
                "status_code": status.HTTP_200_OK,
                "following_count": following_profiles.count(),
                "users_i_follow": serializer.data,
            }
            return Response(formatted_response, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(status=404)


class FollowAPIView(APIView):
    """View for following a profile"""

    def post(self, request, user_id, format=None):
        """Adds the user_id to the request.user following.
        If successful sends success reponse back and emails user.
        Raises exception if same profile or doesn't exist.
        Sends bad request if already following.
        """
        try:
            follower = Profile.objects.get(user=self.request.user)
            user_profile = request.user.profile
            profile = Profile.objects.get(user__id=user_id)

            if profile == follower:
                raise CantFollowYourself()

            if user_profile.check_following(profile):
                formatted_response = {
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "message": f"You are already following {profile.user.first_name} {profile.user.last_name}",
                }
                return Response(formatted_response, status=status.HTTP_400_BAD_REQUEST)

            user_profile.follow(profile)
            subject = "A new user follow you"
            message = f"Hi there, {profile.user.first_name}!!, the user {user_profile.user.first_name} {user_profile.user.last_name} now follows you"
            from_email = DEFAULT_FROM_EMAIL
            recipient_list = [profile.user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)
            return Response(
                {
                    "status_code": status.HTTP_200_OK,
                    "message": f"You are now following {profile.user.first_name} {profile.user.last_name}",
                }
            )
        except Profile.DoesNotExist:
            raise NotFound("You can't follow a profile that does not exist.")


class UnfollowAPIView(APIView):
    """View for unfollowing an user profile"""

    def post(self, request, user_id, *args, **kwargs):
        """Unfollows a user and returns unfollow message and ok status.
        If request.user is not following user_id returns bad request and error message.
        """
        user_profile = request.user.profile
        profile = Profile.objects.get(user__id=user_id)

        if not user_profile.check_following(profile):
            formatted_response = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": f"You can't unfollow {profile.user.first_name} {profile.user.last_name}, since you were not following them in the first place",
            }
            return Response(
                formatted_response,
                status.HTTP_400_BAD_REQUEST,
            )
        user_profile.unfollow(profile)
        formatted_response = {
            "status_code": status.HTTP_200_OK,
            "message": f"You have unfollowed {profile.user.first_name} {profile.user.last_name}",
        }
        return Response(formatted_response, status.HTTP_200_OK)
