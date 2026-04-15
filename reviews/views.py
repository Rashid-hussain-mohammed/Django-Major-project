from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from .models import Review
from .serializers import ReviewSerializer

# 1. Reviews API (With ML Interceptor)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Grab the raw text the customer just typed
        feedback = serializer.validated_data.get('feedback_text', '')
        
        # Run the VADER Sentiment Analysis
        analyzer = SentimentIntensityAnalyzer()
        sentiment_dict = analyzer.polarity_scores(feedback)
        
        # The 'compound' score is the overall metric (-1.0 to 1.0)
        ai_score = sentiment_dict['compound']
        
        # Save the review to the database, injecting the score!
        serializer.save(sentiment_score=ai_score)