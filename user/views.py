from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User, UserFollowing
from user.serializers import (
    UserSerializer,
    UserFollowingSerializer,
    UserFollowersSerializer,
    UserDetailSerializer,
)


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class UpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class DetailUserView(generics.RetrieveAPIView):
    serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer


class UserFollowingView(viewsets.ModelViewSet):
    serializer_class = UserFollowingSerializer
    queryset = UserFollowing.objects.all()


class UserFollow(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        user = request.user
        follow = self.get_object(pk)
        UserFollowing.objects.create(user_id=user, following_user_id = follow)
        serializer = UserSerializer(follow)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        user = request.user
        follow = self.get_object(pk)
        connection = UserFollowing.objects.filter(user_id=user, following_user_id = follow).first()
        connection.delete()
        serializer = UserSerializer(follow)
        return Response(serializer.data)