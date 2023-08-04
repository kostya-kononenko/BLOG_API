from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "password",
            "email",
            "avatar",
            "bio",
            "date_of_birth",
            "facebook_url",
            "twitter_url",
            "instagram_url",
        )
        read_only_fields = ("id", "is_stuff")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

        @staticmethod
        def create(self, validated_data):
            return get_user_model().objects.create_user(**validated_data)

        @staticmethod
        def update(self, instance, validated_data):
            password = validated_data.pop("password", None)
            user = super().update(instance, validated_data)

            if password:
                user.set_password(password)
                user.save()

            return user
