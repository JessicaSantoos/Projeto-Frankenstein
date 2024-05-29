from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='login', permanent=False)),
    path('users/', include('users.urls')),
    path('home/', include('home.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)