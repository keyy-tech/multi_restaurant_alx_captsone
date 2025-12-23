from django.urls import path
from .views import (
    UserRegistrationView,
    UserUpdateView,
    AdminUpdateRoleView,
)

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("me/", UserUpdateView.as_view(), name="update"),
    path(
        "update-role/<int:user_id>/", AdminUpdateRoleView.as_view(), name="update-role"
    ),
]
