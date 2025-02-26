import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

import chat.routing  # import your chat app's websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')
django.setup()

# ASGI app that serves HTTP (including static files) via ASGIStaticFilesHandler
django_asgi_app = ASGIStaticFilesHandler(get_asgi_application())

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # All HTTP (including admin, static files, etc.)
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # your chat routes
        )
    ),
})