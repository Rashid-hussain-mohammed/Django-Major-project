from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Dish, Order, Review
from .serializers import DishSerializer, OrderSerializer, ReviewSerializer
#from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from rest_framework.permissions import AllowAny

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
    permission_classes = [IsAuthenticatedOrReadOnly]

# 2. Orders API (For placing and tracking orders)
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

# 3. Reviews API (With ML Interceptor)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Grab the raw text the customer just typed
        feedback = serializer.validated_data.get('feedback_text', '')
        
        # 2. Run the VADER Sentiment Analysis
        # Initialize the VADER analyzer
        analyzer = SentimentIntensityAnalyzer()
        
        # This returns a dictionary of scores: {'neg': 0.0, 'neu': 0.5, 'pos': 0.5, 'compound': 0.8}
        sentiment_dict = analyzer.polarity_scores(feedback)
        
        # The 'compound' score is the overall metric from -1.0 (extremely negative) to 1.0 (extremely positive)
        ai_score = sentiment_dict['compound']
        
        # 3. Save the review to the database, injecting the VADER AI score automatically!
        serializer.save(sentiment_score=ai_score)