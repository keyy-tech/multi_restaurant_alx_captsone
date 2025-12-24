from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    get_object_or_404,
    GenericAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restaurants.models import Menu
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializers


@extend_schema(tags=["Cart"])
class CartListDestroy(GenericAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        return get_object_or_404(Cart, pk=self.kwargs["pk"], user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = {
            "msg": "Cart retrieved successfully",
            "data": serializer.data,
            "count": queryset.count(),
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=["Cart"])
class CartItemsCreateListAPIView(CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(cart=cart, data=request.data)
        serializer.is_valid(raise_exception=True)

        menu = serializer.validated_data["menu"]
        quantity = serializer.validated_data.get("quantity", 1)

        if not get_object_or_404(Menu, id=menu.id):
            data = {
                "msg": "Menu not found",
                "data": [],
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)

        cart_items, created = CartItem.objects.get_or_create(
            cart=cart, menu=menu, quantity=quantity
        )
        if not created:
            cart_items.quantity += 1
        else:
            cart_items.quantity = quantity

        serializer = self.get_serializer(cart_items, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            "msg": "Item added successfully",
            "data": serializer.data,
            "status": True,
        }

        return Response(data, status=status.HTTP_201_CREATED)


@extend_schema(tags=["Cart"])
class CartItemUpdateDestroyAPIView(GenericAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Cart, pk=self.kwargs["pk"], user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "msg": "Item updated successfully",
            "data": serializer.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
