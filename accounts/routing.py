from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Manager Dashboard connects here: ws://localhost:8000/ws/dashboard/2/
    re_path(r'ws/dashboard/(?P<restaurant_id>\w+)/$', consumers.DashboardConsumer.as_asgi()),
    
    # Chat boxes connect here: ws://localhost:8000/ws/chat/15/
    re_path(r'ws/chat/(?P<order_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]