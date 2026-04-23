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

from .models import Dish, Order, Table
from .serializers import DishSerializer, OrderSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .serializers import TableSerializer

User = get_user_model()

def home(request):
    return HttpResponse("""
        <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1>🚀 M4 Server is Live!</h1>
            <p>Identity & Access Management Portal</p>
        </div>
    """)

# 1. Menu API (Customers can only read this, not edit)
class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        # 1. NEW: Check if the frontend sent a secret UUID
        table_uuid = self.request.query_params.get('table_uuid')
        if table_uuid:
            try:
                # Find the table using the secret code
                table = Table.objects.get(secure_id=table_uuid)
                # Return the dishes for the manager who owns this table
                return Dish.objects.filter(owner=table.restaurant, is_available=True)
            except Table.DoesNotExist:
                return Dish.objects.none()

        # 2. Manager Dashboard Fallback
        if self.request.user.is_authenticated:
            return Dish.objects.filter(owner=self.request.user)
            
        return Dish.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
# 2. Orders API (For placing and tracking orders)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Order.objects.filter(owner=self.request.user).order_by('-created_at')
        return Order.objects.none()

    def perform_create(self, serializer):
        # NEW: The frontend now sends the UUID when placing an order
        table_uuid = self.request.data.get('table_uuid')
        try:
            table = Table.objects.get(secure_id=table_uuid)
            # We securely link the order to both the Table AND the Manager
            serializer.save(owner=table.restaurant, table=table)
        except Table.DoesNotExist:
            pass # In a production app, we'd throw an error here

class TableViewSet(viewsets.ModelViewSet):
    serializer_class = TableSerializer
    
    def get_queryset(self):
        # Only show the manager their own tables
        if self.request.user.is_authenticated:
            return Table.objects.filter(restaurant=self.request.user).order_by('number')
        return Table.objects.none()

    def perform_create(self, serializer):
        # When creating a table, auto-assign it to the logged-in manager
        serializer.save(restaurant=self.request.user)
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