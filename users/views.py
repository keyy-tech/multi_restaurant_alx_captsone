from drf_spectacular.utils import extend_schema
from rest_framework import status, generics
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import User, UserProfile
from .serializers import (
    UserSerializer,
    SuperUserSerializer,
    UpdateRoleSerializers,
    UserProfileSerializer,
)


# ---------------------------
# User Registration
# ---------------------------
@extend_schema(
    request={...},  # Keep your existing extend_schema definition
    tags=["Users"],
    summary="Register a new user account",
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


# ---------------------------
# User Update / Retrieve / Delete
# ---------------------------
@extend_schema(
    tags=["Users"], summary="Retrieve, update, or delete the authenticated user"
)
class UserUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "msg": "User retrieved successfully",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

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
        return Response(
            {"msg": "User deleted successfully", "status": True},
            status=status.HTTP_204_NO_CONTENT,
        )


# ---------------------------
# UserProfile Update
# ---------------------------
@extend_schema(tags=["Users"], summary="Update the authenticated user's profile")
class UserProfileUpdateAPIView(UpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.user_profile

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "msg": "User profile updated successfully",
                "data": response.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )


# ---------------------------
# Admin Update Role
# ---------------------------
@extend_schema(tags=["Users"], summary="Admin update a user's role")
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
                {"msg": "User is already an owner.", "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )
        response = super().update(request, *args, **kwargs)
        return Response(
            {"msg": "Role updated successfully", "data": response.data, "status": True},
            status=status.HTTP_200_OK,
        )


# ---------------------------
# JWT Views
# ---------------------------
@extend_schema(
    tags=["Authentication"], summary="Obtain a JWT access and refresh token pair"
)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass


@extend_schema(
    tags=["Authentication"], summary="Refresh a JWT access token using a refresh token"
)
class CustomTokenRefreshView(TokenRefreshView):
    pass


# ---------------------------
# SuperUser Creation
# ---------------------------
@extend_schema(tags=["Super Users"], summary="Create a new superuser account")
class CreateSuperUserView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SuperUserSerializer

    def create(self, request: Request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "msg": "You have successfully been created as a superuser",
                "data": response.data,
                "status": True,
            },
            status=status.HTTP_201_CREATED,
        )


# ---------------------------
# List All Users
# ---------------------------
@extend_schema(tags=["Super Users"], summary="List all users (admin only)")
class ListUsersView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def list(self, request: Request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response(
            {
                "msg": "Users retrieved successfully",
                "data": response.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )


# ---------------------------
# Update / Retrieve / Delete SuperUser
# ---------------------------
@extend_schema(
    tags=["Super Users"],
    summary="Retrieve, update, or delete the authenticated superuser",
)
class UpdateRetrieveDestroySuperUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        return self.request.user  # Return User, not UserProfile

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
            {
                "msg": "User retrieved successfully",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request: Request, *args, **kwargs):
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

    def destroy(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {"msg": "User deleted successfully", "status": True},
            status=status.HTTP_204_NO_CONTENT,
        )
