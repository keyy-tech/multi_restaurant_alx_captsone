from django.urls import path

from .views import RestaurantsView, RestaurantsDetailView, MenuView, MenuDetailView

urlpatterns = [
    # Restaurants
    path("", RestaurantsView.as_view(), name="restaurants-list-create"),
    path("<int:pk>/", RestaurantsDetailView.as_view(), name="restaurants-detail"),
    # Menu for a specific restaurant
    path("<int:pk>/menu/", MenuView.as_view(), name="menu-list-create"),
    path("<int:pk>/menu/<int:menu_pk>/", MenuDetailView.as_view(), name="menu-detail"),
]
