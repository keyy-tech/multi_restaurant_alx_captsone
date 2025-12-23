from django.urls import path
from .views import RestaurantsView, RestaurantsUpdateView, MenuView, MenuUpdateView

urlpatterns = [
    path("", RestaurantsView.as_view(), name="restaurants"),
    path("<int:pk>/", RestaurantsUpdateView.as_view(), name="restaurants-update"),  
    path("<int:pk>/menu/", MenuView.as_view(), name="menu"),
    path("<int:pk>/menu/<int:menu_pk>/", MenuUpdateView.as_view(), name="menu-update"),
]