from django.urls import path

from .views import CartCreateListView, CartUpdateDeleteView

urlpatterns = [
    path("", CartCreateListView.as_view(), name="cart_create"),
    path("<int:pk>/", CartUpdateDeleteView.as_view(), name="cart_detail"),
]
