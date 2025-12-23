from rest_framework import serializers
from .models import Restaurants, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["name", "description", "price", "is_available", "restaurant"]


class RestaurantsSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurants
        fields = ["name", "owner", "description", "address", "phone_number", "menu"]
