from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .models import User
from .serializers import UserSerializer, UpdateRoleSerializers
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema
from rest_framework import generics


@extend_schema(
    request={
        "application/json": {
            "type": "object",
            "properties": {
                "email": {"type": "string"},
                "password": {"type": "string"},
                "first_name": {"type": "string"},
                "last_name": {"type": "string"},
                "user_profile": {
                    "type": "object",
                    "properties": {
                        "other_name": {"type": "string"},
                        "date_of_birth": {"type": "string", "format": "date"},
                        "phone_number": {"type": "string"},
                    },
                },
            },
        }
    },
    tags=["Users"],
)
class UserRegistrationView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request: Request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        data = {
            "msg": "You have successfully created an account",
            "data": response.data,
            "status": True,
        }

        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Users"])
class UserUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        return user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        data = {
            "msg": "User retrieved successfully",
            "data": serializer.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "msg": "User updated successfully",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

        data = {
            "msg": "User deleted successfully",
            "status": True,
        }

        return Response(data, status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Users"])
class AdminUpdateRoleView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateRoleSerializers
    permission_classes = [IsAdminUser]

    def get_object(self):
        user_id = self.kwargs.get("user_id")
        return generics.get_object_or_404(User, id=user_id)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.role == "owner":
            return Response(
                {
                    "msg": "User is already an owner.",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        response = super().update(request, *args, **kwargs)

        data = {
            "msg": "Role updated successfully",
            "data": response.data,
            "status": True,
        }

        return Response(data, status=status.HTTP_204_NO_CONTENT)
