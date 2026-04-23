from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, OrderViewSet, ai_order_parser, register_user, login_user, TableViewSet
from reviews.views import ReviewViewSet # Import from reviews!

router = DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet) # Connects the extracted view
# Add this line right next to your other router.register lines!
router.register(r'tables', TableViewSet, basename='table')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/ai-order/', ai_order_parser, name='ai-order-parser'), 
    path('api/register/', register_user, name='register'),
    path('api/login/', login_user, name='login'),
]