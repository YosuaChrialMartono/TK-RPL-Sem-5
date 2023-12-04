from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authuser.urls')),
    path('mentor/', include('mentor.urls')),
    path('user/', include('UserProfile.urls')),
    path('kelas/', include('kelas.urls')),
    path('mentee/', include('mentee.urls')),
    path('review/', include('review.urls')),
    path('adminreview/', include('adminreview.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)