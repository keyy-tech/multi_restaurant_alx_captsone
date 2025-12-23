from os import read
from rest_framework import serializers
from .models import User, UserProfile
from django.db import transaction


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            "other_name",
            "date_of_birth",
            "phone_number",
        ]
        read_only_fields = ["user"]


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "first_name",
            "last_name",
            "role",
            "user_profile",
        ]
        read_only_fields = ["id", "is_active", "is_staff", "is_superuser"]

    def create(self, validated_data):
        with transaction.atomic():
            user_profile_data = validated_data.pop("user_profile", None)
            user = User.objects.create_user(**validated_data)
            UserProfile.objects.create(user=user, **user_profile_data)
        return user


class UpdateRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]
