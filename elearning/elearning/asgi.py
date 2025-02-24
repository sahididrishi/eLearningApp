import os
import django
from django.core.asgi import get_asgi_application
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elearning.settings')
django.setup()
application = get_asgi_application()
application = ASGIStaticFilesHandler(application)