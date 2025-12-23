from webbrowser import get
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import restaurants
from .models import Restaurants, Menu
from .serializers import RestaurantsSerializer, MenuSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import get_object_or_404
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
)


class RestaurantsView(ListCreateAPIView):
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


class RestaurantsUpdateView(RetrieveUpdateDestroyAPIView):
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




class MenuView(CreateAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        restaurant = get_object_or_404(Restaurants, pk=self.kwargs.get("pk"), owner=self.request.user)
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
    


class MenuUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get("pk", None)
        user = self.request.user
        menu = get_object_or_404(Menu, pk=pk, restaurant__owner=user)
        return menu

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user.restaurant)

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
