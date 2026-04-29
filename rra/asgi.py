import os
from django.core.asgi import get_asgi_application

# 1. Point to the correct settings folder ('rra' instead of 'my_django_site')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rra.settings')

# 2. Wake up Django BEFORE doing anything else!
django_asgi_app = get_asgi_application()

# 3. Now it's safe to import Channels and your routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from accounts import routing 

# 4. Route the traffic to either normal HTTP or WebSockets
application = ProtocolTypeRouter({
    "http": django_asgi_app, 
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})