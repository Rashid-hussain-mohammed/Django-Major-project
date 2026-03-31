from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# 1. THE USER MODEL (Updated for Restaurant Logic)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_manager = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({'Manager' if self.is_manager else 'Customer'})"

# 2. THE RESTAURANT TABLES
class Table(models.Model):
    number = models.IntegerField(unique=True)
    # In a real app, this holds the URL the QR code points to
    qr_url = models.URLField(blank=True, null=True) 

    def __str__(self):
        return f"Table {self.number}"

# 3. THE MENU
class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2) # e.g., 9999.99
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# 4. THE ORDER LIFECYCLE
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending (Ordering)'),
        ('PREPARING', 'Preparing in Kitchen'),
        ('SERVED', 'Served to Table'),
        ('PAID', 'Paid & Completed'),
    ]
    
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.number} - {self.status}"

# 5. THE ITEMS INSIDE AN ORDER (Many-to-Many resolution)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.dish.name} (Order #{self.order.id})"

# 6. THE ML FEEDBACK CORE
class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE) # One review per order
    service_rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)]) # 1 to 10
    food_rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)]) # 1 to 10
    feedback_text = models.TextField()
    
    # This is the field our NLP Model will fill in automatically later!
    sentiment_score = models.FloatField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Order #{self.order.id} - Sentiment: {self.sentiment_score}"