from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Restaurants, Menu
from .serializers import RestaurantsSerializer, MenuSerializer, MenuDetailSerializer


# ---------------- RESTAURANTS ----------------


@extend_schema(tags=["Restaurants"])
class RestaurantsView(ListCreateAPIView):
    """
    Unified API endpoint for restaurants.
    - Owners: list their restaurants and create new ones.
    - Customers: list all available restaurants.
    """

    queryset = Restaurants.objects.all()
    serializer_class = RestaurantsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "owner":
            return Restaurants.objects.filter(owner=user)
        return Restaurants.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        msg = (
            "Your Restaurants"
            if request.user.role == "owner"
            else "Available Restaurants"
        )
        return Response(
            {"msg": msg, "data": serializer.data, "status": True},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "owner":
            return Response(
                {"msg": "Only owners can create restaurants", "status": False},
                status=status.HTTP_403_FORBIDDEN,
            )

        if Restaurants.objects.filter(
            owner=user, name=request.data.get("name")
        ).exists():
            return Response(
                {"msg": "You already have a restaurant", "status": False},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "msg": "Restaurant created successfully",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_201_CREATED,
        )


# ---------------- RESTAURANT DETAIL ----------------


@extend_schema(tags=["Restaurants"])
class RestaurantsDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = RestaurantsSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        pk = self.kwargs.get("pk")
        user = self.request.user
        if user.role == "owner":
            return get_object_or_404(Restaurants, pk=pk, owner=user)
        return get_object_or_404(Restaurants, pk=pk)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                "msg": "Restaurant retrieved successfully",
                "data": response.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "msg": "Restaurant updated successfully",
                "data": response.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {"msg": "Restaurant deleted successfully", "status": True},
            status=status.HTTP_204_NO_CONTENT,
        )


# ---------------- MENU ----------------


@extend_schema(tags=["Menu"])
class MenuView(ListCreateAPIView):
    """
    Unified menu endpoint.
    - Owners: create and list menus of their restaurant.
    - Customers: list menu items (read-only).
    """

    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return (
            MenuSerializer
            if self.request.user.role == "owner"
            else MenuDetailSerializer
        )

    def get_queryset(self):
        restaurant_id = self.kwargs.get("pk")
        user = self.request.user
        if user.role == "owner":
            return Menu.objects.filter(
                restaurant__id=restaurant_id, restaurant__owner=user
            )
        return Menu.objects.filter(restaurant__id=restaurant_id, is_available=True)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(
            {"msg": "Menu Items", "data": serializer.data, "status": True},
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "owner":
            return Response(
                {"msg": "Only owners can create menu items", "status": False},
                status=status.HTTP_403_FORBIDDEN,
            )

        restaurant = get_object_or_404(
            Restaurants, pk=self.kwargs.get("pk"), owner=user
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(restaurant=restaurant)
        return Response(
            {
                "msg": "Menu item created successfully",
                "data": serializer.data,
                "status": True,
            },
            status=status.HTTP_201_CREATED,
        )


# ---------------- MENU DETAIL ----------------


@extend_schema(tags=["Menu"])
class MenuDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return (
            MenuSerializer
            if self.request.user.role == "owner"
            else MenuDetailSerializer
        )

    def get_object(self):
        pk = self.kwargs.get("pk")
        user = self.request.user
        if user.role == "owner":
            return get_object_or_404(Menu, pk=pk, restaurant__owner=user)
        return get_object_or_404(Menu, pk=pk, is_available=True)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response(
            {
                "msg": "Menu item retrieved successfully",
                "data": response.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def update(self, request, *args, **kwargs):
        if self.request.user.role != "owner":
            return Response(
                {"msg": "Only owners can update menu items", "status": False},
                status=status.HTTP_403_FORBIDDEN,
            )
        response = super().update(request, *args, **kwargs)
        return Response(
            {
                "msg": "Menu item updated successfully",
                "data": response.data,
                "status": True,
            },
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, *args, **kwargs):
        if self.request.user.role != "owner":
            return Response(
                {"msg": "Only owners can delete menu items", "status": False},
                status=status.HTTP_403_FORBIDDEN,
            )
        super().destroy(request, *args, **kwargs)
        return Response(
            {"msg": "Menu item deleted successfully", "status": True},
            status=status.HTTP_204_NO_CONTENT,
        )
