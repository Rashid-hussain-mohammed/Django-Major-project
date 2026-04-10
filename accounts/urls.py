from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, OrderViewSet, ai_order_parser # Import from accounts
from reviews.views import ReviewViewSet # Import from reviews!

router = DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet) # Connects the extracted view

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/ai-order/', ai_order_parser, name='ai-order-parser'), 
]