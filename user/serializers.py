from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from django.utils.translation import gettext as _

from user.models import UserFollowing


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "bio",
            "date_of_birth",
            "facebook_url",
            "twitter_url",
            "instagram_url",
        )
        read_only_fields = ("id", "is_stuff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserDetailSerializer(UserSerializer):
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "bio",
            "date_of_birth",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "following",
            "followers",
        )

    def get_following(self, obj):
        return UserFollowingSerializer(obj.following.all(), many=True).data

    def get_followers(self, obj):
        return UserFollowersSerializer(obj.followers.all(), many=True).data


class UserFollowingSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source="following_user_id.id")
    first_name = serializers.ReadOnlyField(
        source="following_user_id.first_name")
    last_name = serializers.ReadOnlyField(
        source="following_user_id.last_name")

    class Meta:
        model = UserFollowing
        fields = ("id", "first_name", "last_name")


class UserFollowersSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source="user_id.first_name")
    last_name = serializers.ReadOnlyField(source="user_id.last_name")

    class Meta:
        model = UserFollowing
        fields = ("user_id", "first_name", "last_name")


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(email=email, password=password)

            if user:
                if not user.is_active:
                    msg = _("User account is disabled.")
                    raise serializers.ValidationError(
                        msg, code="authorization")
            else:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(
                    msg, code="authorization")
        else:
            msg = _("Must include 'username' and 'password'.")
            raise serializers.ValidationError(
                msg, code="authorization")

        attrs["user"] = user
        return attrs
