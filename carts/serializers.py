from rest_framework import serializers

from .models import Cart


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "menu",
            "quantity",
        ]
        read_only_fields = ["total_price", "added_at", "updated_at"]
