from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from carts.models import Cart
from orders.models import OrderItem, Order
from orders.serializers import OrderSerializer


class OrderCreateView(ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = None
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Cart.objects.exists()

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        if not instance:
            data = {
                "msg": "You cannot create an order with empty cart.",
                "status": False,
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        cart = Cart.objects.prefetch_related("items").filter(user=request.user)
        cart.calculate_total_price()

        order = Order.objects.create(
            user=request.user, cart=cart, total_amount=total_price
        )

        order_item_create_list = []

        for item in cart.item.all():
            order_item_create_list.append(
                OrderItem.objects.create(
                    order=item.order,
                    item=item.item,
                    quantity=item.quantity,
                    price=item.cart_item_price(),
                )
            )

        OrderItem.objects.bulk_create(order_item_create_list)

        cart.delete()
        serializer = self.serializer_class(order)

        data = {
            "msg": "Order created successfully.",
            "data": serializer.data,
            "status": True,
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        data = {
            "msg": "Order list created successfully.",
            "data": response.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"], user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.status in ["processing", "completed"]:
            return Response(
                {
                    "msg": "Order already processed.",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer.save(user=self.request.user)
        return None

    def perform_destroy(self, instance):
        instance = self.get_object()
        if instance.status == "completed":
            return Response(
                {
                    "msg": "Order is already completed.",
                    "status": False,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        instance.delete()
        return None

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        data = {
            "msg": "Order updated successfully.",
            "data": serializer.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        data = {
            "msg": "Order retrieved successfully.",
            "data": response.data,
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        data = {
            "msg": "Order deleted successfully.",
            "status": True,
        }
        return Response(data, status=status.HTTP_200_OK)
