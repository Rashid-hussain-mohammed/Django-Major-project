from django.db import models
from accounts.models import Order 
from django.conf import settings # <-- 1. ADD THIS IMPORT

# 6. THE ML FEEDBACK CORE
class Review(models.Model):
    # 2. ADD THIS LINE: Connect the review to the restaurant owner
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE) # One review per order
    service_rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)]) # 1 to 10
    food_rating = models.IntegerField(choices=[(i, i) for i in range(1, 11)]) # 1 to 10
    feedback_text = models.TextField()
    
    sentiment_score = models.FloatField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Order #{self.order.id} - Sentiment: {self.sentiment_score}"