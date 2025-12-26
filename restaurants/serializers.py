from rest_framework import serializers

from .models import Restaurants, Menu


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "name", "price", "description", "is_available"]


class MenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ["id", "name", "price", "description"]
        read_only_fields = ["id", "name", "price", "description"]


class RestaurantsSerializer(serializers.ModelSerializer):
    menu = MenuSerializer(many=True, required=False)

    class Meta:
        model = Restaurants
        fields = ["id", "name", "description", "address", "phone_number", "menu"]

    def create(self, validated_data):
        menu_data = validated_data.pop("menu", [])
        restaurant = Restaurants.objects.create(
            owner=self.context["request"].user, **validated_data
        )
        for item in menu_data:
            Menu.objects.create(restaurant=restaurant, **item)
        return restaurant
