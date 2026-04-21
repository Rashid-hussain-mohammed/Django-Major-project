from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import re

# Auth Imports
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import status

from .models import Dish, Order
from .serializers import DishSerializer, OrderSerializer

User = get_user_model()

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
# --- IDENTITY & ACCESS MANAGEMENT (Auth) ---

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the email is already registered
    if User.objects.filter(email=email).exists():
        return Response({"error": "This email is already in use."}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user using your CustomUser fields
    user = User.objects.create_user(username=username, email=email, password=password)
    
    # IMPORTANT: Since they are signing up via the SaaS Landing Page, make them a manager!
    user.is_manager = True 
    user.is_customer = False
    user.save()
    
    # Generate an API token for the new restaurant owner
    token, created = Token.objects.get_or_create(user=user)
    
    return Response({
        "token": token.key, 
        "message": "Restaurant account created successfully!"
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    # Because your USERNAME_FIELD is 'email', we extract the email to log them in
    email = request.data.get('email') 
    password = request.data.get('password')

    # Django's authenticate will map the 'email' to your CustomUser's USERNAME_FIELD
    user = authenticate(request, email=email, password=password)
    
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key, 
            "username": user.username,
            "is_manager": user.is_manager # Let Angular know they are a restaurant owner
        })
    else:
        return Response({"error": "Invalid email or password."}, status=status.HTTP_401_UNAUTHORIZED)