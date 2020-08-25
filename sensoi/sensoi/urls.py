from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls import url, include

schema_view = get_schema_view(
    openapi.Info(
        title="Ideeza API",
        default_version='v1',
        description="Ideeza API for development",
        terms_of_service="https://ideeza.com/policies/terms/",
        contact=openapi.Contact(email="support@ideeza.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/',include('user.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Ideeza Admin'
admin.site.site_title = 'Ideeza Site Admin'
admin.site.index_title = 'Welcome to Ideeza Admin Dashboard'