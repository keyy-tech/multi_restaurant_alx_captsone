from django.db import models

from restaurants.models import Menu
from users.models import User


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def item_total_price(self):
        return self.menu.price * self.quantity

    def calculate_total_price(self):
        cart_items = Cart.objects.filter(user=self.user)
        total = sum(item.item_total_price() for item in cart_items)
        return total
