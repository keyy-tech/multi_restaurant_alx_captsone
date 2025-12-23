from rest_framework import status
from rest_framework.response import Response
from .models import Restaurants, Menu
from .serializers import RestaurantsSerializer, MenuSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)
from drf_spectacular.utils import  extend_schema


@extend_schema(tags=["Restaurants"])
class RestaurantsView(ListCreateAPIView):
    """
    API endpoint for listing and creating restaurants for the authenticated user.

    GET:
        Returns a list of restaurants owned by the logged-in user.
    POST:
        Creates a new restaurant for the authenticated user.
        Validates that the user does not already have a restaurant with the same name.
    """

    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Restaurants.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = {"msg": "Your Restaurants", "data": response.data, "status": True}
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if Restaurants.objects.filter(
            owner=request.user, name=request.data.get("name")
        ).exists():
            data = {
                "msg": "You already have a restaurant",
                "status": False,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)
        data = {
            "msg": "Restaurant created successfully",
            "data": response.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Restaurants"])
class RestaurantsUpdateView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting a single restaurant owned by the authenticated user.

    GET:
        Retrieve details of a single restaurant.
    PUT/PATCH:
        Update a restaurant owned by the authenticated user.
    DELETE:
        Delete a restaurant owned by the authenticated user.
    """

    serializer_class = RestaurantsSerializer
    permission_classes = [IsAuthenticated]
    queryset = Restaurants.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk", None)
        user = self.request.user
        restaurant = get_object_or_404(Restaurants, pk=pk, owner=user)
        return restaurant

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = {
            "msg": "",
            "data": response.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        data = {
            "msg": "Restaurant deleted successfully",
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        data = {
            "msg": "Restaurant retrieved successfully",
            "data": response.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)


@extend_schema(tags=["Menu"])
class MenuView(CreateAPIView):
    """
    API endpoint for creating a menu item for a specific restaurant.

    POST:
        Creates a new menu item for the restaurant specified by the 'pk' in the URL.
        Ensures that the restaurant belongs to the authenticated user.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        restaurant = get_object_or_404(
            Restaurants, pk=self.kwargs.get("pk"), owner=self.request.user
        )
        return restaurant

    def perform_create(self, serializer):
        serializer.save(restaurant=self.get_object())

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        data = {
            "msg": "Menu created successfully",
            "data": response.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Menu"])
class MenuUpdateView(RetrieveUpdateDestroyAPIView):
    """
    API endpoint for retrieving, updating, and deleting menu items for restaurants owned by the authenticated user.

    GET:
        Retrieve details of a specific menu item.
    PUT/PATCH:
        Update a menu item.
    DELETE:
        Delete a menu item.
    """

    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get("pk", None)
        user = self.request.user
        menu = get_object_or_404(Menu, pk=pk, restaurant__owner=user)
        return menu

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        data = {
            "msg": "Menu updated successfully",
            "data": response.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        data = {
            "msg": "Menu deleted successfully",
            "status": True,
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        data = {
            "msg": "Menu retrieved successfully",
            "data": response.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)
