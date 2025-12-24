from django.urls import path

from .views import (
    CartListDestroy,
    CartItemUpdateDestroyAPIView,
    CartItemsCreateListAPIView,
)

urlpatterns = [
    path("", CartListDestroy.as_view()),
    path("cart_items/", CartItemsCreateListAPIView.as_view()),
    path("cart_items/<int:pk>/", CartItemUpdateDestroyAPIView.as_view()),
]
