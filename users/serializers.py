from os import read
from rest_framework import serializers
from .models import User, UserProfile
from django.db import transaction
from django.contrib.auth.password_validation import validate_password


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
    password = serializers.CharField(write_only=True, required=True)
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "role",
            "user_profile",
            "password"
        ]
        read_only_fields = ["id", "is_active", "is_staff", "is_superuser", "password"]


    def create(self, validated_data):
        with transaction.atomic():
            user_profile_data = validated_data.pop("user_profile", None)
            password = validated_data.pop("password")
            user = User.objects.create_user(**validated_data)
            user.set_password(password)
            user.save()
            UserProfile.objects.create(user=user, **user_profile_data)
        return user


class UpdateRoleSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["role"]
