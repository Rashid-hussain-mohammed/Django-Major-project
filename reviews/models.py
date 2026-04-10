from django.db import models
from accounts.models import Order # We must import Order from the accounts app!

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