from rest_framework.generics import (
    ListCreateAPIView,
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
)

from carts.serializers import CartSerializer
from restaurants.models import Menu
from .models import Cart


class CartCreateListView(ListCreateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        data = {"msg": "Your Cart Items", "data": serializer.data, "status": True}
        return Response(data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        menu = get_object_or_404(Menu, pk=request.data.get("menu"))
        if menu.quantity < 1:
            data = {
                "msg": "Menu item is out of stock",
                "status": False,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data.get("quantity", 1)

        if int(quantity) > menu.quantity:
            data = {
                "msg": "Requested quantity exceeds available stock",
                "status": False,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(user=request.user, menu=menu)

        if not created:
            cart.quantity += quantity
        else:
            cart.quantity = quantity

        cart.total_price = cart.calculate_total_price()
        cart.save()

        serializer = self.get_serializer(cart)

        data = {
            "msg": "Cart item added successfully",
            "data": serializer.data,
            "total_price": cart.cart_item_price(),
            "status": True,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class CartUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_object(self):
        pk = self.kwargs.get("pk", None)
        user = self.request.user
        cart = get_object_or_404(Cart, pk=pk, user=user)
        return cart

    def update(self, request, *args, **kwargs):
        cart = self.get_object()
        menu = cart.menu
        quantity = request.data.get("quantity", cart.quantity)

        if int(quantity) > menu.quantity:
            data = {
                "msg": "Requested quantity exceeds available stock",
                "status": False,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        response = super().update(request, *args, **kwargs)
        cart.total_price = cart.calculate_total_price()
        cart.save()

        data = {
            "msg": "Cart item updated successfully",
            "data": response.data,
            "total_price": cart_item.cart_item_price(),
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        cart = self.get_object()
        super().destroy(request, *args, **kwargs)
        data = {
            "msg": "Cart item deleted successfully",
            "total_price": cart.cart_item_price(),
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        cart = self.get_object()
        data = {
            "msg": "Cart item retrieved successfully",
            "data": response.data,
            "total_price": cart.cart_item_price(),
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)
