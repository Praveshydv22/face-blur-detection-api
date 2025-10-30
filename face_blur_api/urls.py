from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/blur/', include('blur_detector.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
