from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Dish, Order, Review
from .serializers import DishSerializer, OrderSerializer, ReviewSerializer

def home(request):
    return HttpResponse("""
        <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1>🚀 M4 Server is Live!</h1>
            <p>Identity & Access Management Portal</p>
        </div>
    """)
# 1. Menu API (Customers can only read this, not edit)
class DishViewSet(viewsets.ReadOnlyModelViewSet):
    # Only show dishes that are actually available!
    queryset = Dish.objects.filter(is_available=True) 
    serializer_class = DishSerializer

# 2. Orders API (For placing and tracking orders)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# 3. Reviews API (Where the ML will intercept data later)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer