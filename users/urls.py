from django.urls import path

from .views import (
    UserRegistrationView,
    UserUpdateView,
    AdminUpdateRoleView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CreateSuperUserView,
    UserProfileUpdateAPIView,
    ListUsersView,
    UpdateRetrieveDestroySuperUserView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("me/", UserUpdateView.as_view(), name="update"),
    path("profile/", UserProfileUpdateAPIView.as_view(), name="profile"),
    path(
        "update-role/<int:user_id>/", AdminUpdateRoleView.as_view(), name="update-role"
    ),
    path("super_users/", CreateSuperUserView.as_view(), name="superuser-register"),
    path("super_users/users/", ListUsersView.as_view(), name="superuser-list"),
    path(
        "super_users/me/",
        UpdateRetrieveDestroySuperUserView.as_view(),
        name="superuser-update",
    ),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]
