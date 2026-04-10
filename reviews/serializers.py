from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        # This tells the API: "Don't let the user submit these; the backend handles them."
        read_only_fields = ['sentiment_score', 'created_at']