from django.contrib import admin
from .models import Review

# This safely registers the Review model from its new home
admin.site.register(Review)