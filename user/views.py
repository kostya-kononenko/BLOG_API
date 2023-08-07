from rest_framework import generics, viewsets
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import User, UserFollowing
from user.serializers import UserSerializer, FollowingSerializer, FollowersSerializer, UserDetailSerializer


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


class UserFollowingViewSet(viewsets.ModelViewSet):
    serializer_class = FollowingSerializer
    queryset = UserFollowing.objects.all()


class UserFollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowersSerializer
    queryset = UserFollowing.objects.all()
