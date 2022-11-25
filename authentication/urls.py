from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # path('', include('social_django.urls', namespace='social')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api-accounts/', include('accounts.urls')),
]
