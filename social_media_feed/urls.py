# social_media/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Core App (Main functionality)
    path('', include('core.urls')),

    # Django Admin
    path('admin/', admin.site.urls),
]

# Media Files Routing (Only for development)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
