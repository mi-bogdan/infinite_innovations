from django.contrib import admin
from django.urls import path, include
from config import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('idea.urls')),
    path('auth/', include('authentications.urls')),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
