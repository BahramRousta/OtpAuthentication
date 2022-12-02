from django.contrib import admin
from django.urls import path, include
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('auth/', include('drf_social_oauth2.urls', namespace='drf')),
    # path('', include('social_django.urls', namespace='social')),
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('api-accounts/', include('accounts.urls')),
    path('docs/', include_docs_urls(title='AuthenticationAPI')),
    path('schema/', get_schema_view(
        title='AuthenticationAPI',
        description='API for the AuthenticationAPI',
        version='1.0.0',
    ), name='openapi-schema')
]
