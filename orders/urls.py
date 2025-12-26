from django.urls import path

from .views import OrderRetrieveUpdateDestroyAPIView, OrderCreateView

urlpatterns = [
    path("<int:pk>/", OrderRetrieveUpdateDestroyAPIView.as_view()),
    path("", OrderCreateView.as_view()),
]
