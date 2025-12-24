from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "menu_item",
            "quantity",
            "price",
        ]
        read_only_fields = ["added_at", "cart"]


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializers(many=True)

    class Meta:
        model = Cart
        fields = [
            "cart_items",
            "total_price",
        ]

        read_only_fields = ["added_at", "user"]
