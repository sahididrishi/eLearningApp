
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def home(request):
    return render(request, 'home/home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace='users')),

    path('accounts/', include('users.urls', namespace='accounts')),

    path('courses/', include('courses.urls', namespace='courses')),
    path('chat/', include('chat.urls', namespace='chat')),
    path('api/', include('elearning.api_urls')),
    path('', home, name='home'),  # Root URL -> Home page


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)