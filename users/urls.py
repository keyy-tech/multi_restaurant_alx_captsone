from django.urls import path
from .views import (
    UserRegistrationView,
    UserUpdateView,
    AdminUpdateRoleView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    UserProfileUpdateAPIView
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("me/", UserUpdateView.as_view(), name="update"),
    path("profile/", UserProfileUpdateAPIView.as_view(), name="profile"),
    path(
        "update-role/<int:user_id>/", AdminUpdateRoleView.as_view(), name="update-role"
    ),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
