from rest_framework import serializers
from .models import Dish, Order, OrderItem, Table

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'number', 'secure_id']
        read_only_fields = ['secure_id'] # The backend auto-generates this!

class OrderItemSerializer(serializers.ModelSerializer):
    # This automatically grabs the name of the dish so the frontend doesn't just get an ID number
    dish_name = serializers.ReadOnlyField(source='dish.name') 
    dish_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'dish_id', 'dish_name', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    # This nests the items inside the order JSON automatically 
    items = OrderItemSerializer(many=True, required=False) 

    class Meta:
        model = Order
        # Merged the fields and added 'owner' so it matches the database
        fields = ['id', 'owner', 'table', 'status', 'total_price', 'created_at', 'items']
        
        # --- 🚨 THE MAGIC FIX IS SAFELY HERE NOW ---
        read_only_fields = ['owner', 'table']

    def create(self, validated_data):
        # 1. Pull the items list OUT of the order data
        items_data = validated_data.pop('items', [])
        
        # 2. Save the main Order first (so we get an Order ID)
        order = Order.objects.create(**validated_data)
        
        # 3. Loop through the items array and save them to the database
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                dish_id=item_data['dish_id'],
                quantity=item_data['quantity']
            )
            
        return order