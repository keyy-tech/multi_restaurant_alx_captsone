from django.urls import path
from .views import (
    UserRegistrationView,
    UserUpdateView,
    AdminUpdateRoleView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", UserUpdateView.as_view(), name="update"),
    path(
        "update-role/<int:user_id>/", AdminUpdateRoleView.as_view(), name="update-role"
    ),
]
