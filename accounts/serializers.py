from rest_framework import serializers
from .models import Dish, Order, OrderItem, Review

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    # This automatically grabs the name of the dish so the frontend doesn't just get an ID number
    dish_name = serializers.ReadOnlyField(source='dish.name') 
    
    class Meta:
        model = OrderItem
        fields = ['id', 'dish', 'dish_name', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    # This nests the items inside the order JSON automatically
    items = OrderItemSerializer(many=True, read_only=True) 
    
    class Meta:
        model = Order
        fields = ['id', 'table', 'status', 'total_price', 'created_at', 'items']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'