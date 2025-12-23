from rest_framework import serializers
from .models import Restaurants, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["name", "description", "price"]


class RestaurantsSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurants
        fields = ["name", "description", "address", "phone_number", "menu"]
