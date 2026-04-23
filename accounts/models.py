from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import uuid # <--- NEW: For generating unguessable URLs!

# 1. THE USER MODEL (Updated for Restaurant Logic)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_manager = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({'Manager' if self.is_manager else 'Customer'})"

# 2. THE RESTAURANT TABLES (UPGRADED)
class Table(models.Model):
    # 1. Link the table to the specific restaurant manager
    restaurant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # 2. The physical table number (e.g., Table 5)
    # Note: I removed unique=True because multiple restaurants can have a "Table 1"
    number = models.IntegerField()
    
    # 3. The Secret URL Mask (e.g., a1b2c3d4...)
    secure_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Table {self.number} (Restaurant ID: {self.restaurant.id})"

# 3. THE MENU
class Dish(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# 4. THE ORDER LIFECYCLE
class Order(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending (Ordering)'),
        ('PREPARING', 'Preparing in Kitchen'),
        ('SERVED', 'Served to Table'),
        ('PAID', 'Paid & Completed'),
    ]
    
    # We kept the strict database ForeignKey here!
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.number} - {self.status}"

# 5. THE ITEMS INSIDE AN ORDER
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.dish.name} (Order #{self.order.id})"