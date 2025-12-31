from django.db import transaction
from rest_framework import serializers

from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "other_name",
            "date_of_birth",
            "phone_number",
        ]
        read_only_fields = ["user"]  # user is managed automatically


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_profile = UserProfileSerializer(required=False)  # optional

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "user_profile",
            "password",
        ]
        read_only_fields = ["id", "is_active", "is_staff", "is_superuser"]

    def create(self, validated_data):
        user_profile_data = validated_data.pop("user_profile", None)
        password = validated_data.pop("password")

        with transaction.atomic():
            # create user and hash password automatically
            user = User.objects.create_user(password=password, **validated_data)

            if user_profile_data:
                UserProfile.objects.create(user=user, **user_profile_data)

        return user


class SuperUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    user_profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "user_profile",
            "password",
        ]
        read_only_fields = ["id", "is_active", "is_staff", "is_superuser"]

    def create(self, validated_data):
        user_profile_data = validated_data.pop("user_profile", None)
        password = validated_data.pop("password")

        with transaction.atomic():
            # create superuser and hash password automatically
            user = User.objects.create_superuser(password=password, **validated_data)

            if user_profile_data:
                UserProfile.objects.create(user=user, **user_profile_data)

        return user


class UpdateRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]
