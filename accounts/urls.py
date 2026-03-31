from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DishViewSet, OrderViewSet, ReviewViewSet

# DRF Routers automatically generate all the GET, POST, PUT, DELETE routes for us!
router = DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    # This exposes all the routes under /accounts/api/...
    path('api/', include(router.urls)), 
]