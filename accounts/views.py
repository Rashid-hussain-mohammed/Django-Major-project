from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes # New for AI
from rest_framework.response import Response # New for AI
import re # Python's regex tool for the AI

from .models import Dish, Order
from .serializers import DishSerializer, OrderSerializer

def home(request):
    return HttpResponse("""
        <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1>🚀 M4 Server is Live!</h1>
            <p>Identity & Access Management Portal</p>
        </div>
    """)

# 1. Menu API (Customers can only read this, not edit)
class DishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dish.objects.filter(is_available=True) 
    serializer_class = DishSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# 2. Orders API (For placing and tracking orders)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

# 3. AI Order NLP Parser (The "Brain")
@api_view(['POST'])
@permission_classes([AllowAny])
def ai_order_parser(request):
    text = request.data.get('text', '').lower()
    available_dishes = Dish.objects.filter(is_available=True)
    detected_items = []

    for dish in available_dishes:
        dish_name = dish.name.lower()
        if dish_name in text:
            quantity = 1 # Default to 1
            
            # Smart Regex: Look for a number right before the food name!
            match = re.search(rf'(\d+)\s+{re.escape(dish_name)}', text)
            if match:
                quantity = int(match.group(1))

            detected_items.append({
                "id": dish.id,
                "name": dish.name,
                "price": str(dish.price),
                "quantity": quantity
            })

    return Response({"parsed_items": detected_items})