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
        title="Sensai API",
        default_version='v1',
        description="Sensai API for development",
        terms_of_service="https://ideeza.com/policies/terms/",
        contact=openapi.Contact(email="support@ideeza.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

admin.site.site_header = 'Sensai Admin'
admin.site.site_title = 'Sensai Site Admin'
admin.site.index_title = 'Welcome to Sensai Admin Dashboard'

urlpatterns = [
    url(r'^api/', include('user.urls')),
    url(r'^api/', include('product.urls')),
    url(r'^admin', admin.site.urls),
    url(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Ideeza Admin'
admin.site.site_title = 'Ideeza Site Admin'
admin.site.index_title = 'Welcome to Ideeza Admin Dashboard'