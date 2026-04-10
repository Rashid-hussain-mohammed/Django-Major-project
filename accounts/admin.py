from django.contrib import admin
from .models import CustomUser, Table, Dish, Order, OrderItem # Review is completely gone!

# This registers all your tables so the Manager (you) can see them
admin.site.register(CustomUser)
admin.site.register(Table)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(OrderItem)