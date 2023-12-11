from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

# Sets the schema view using drf_yasg openapi Info
schema_view = get_schema_view(
    openapi.Info(
        title="Authors Haven API",
        default_version="v1",
        description="API endpoints for Authors Haven Course",
        contact=openapi.Contact(email="anikethbabu@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    # Sets redoc/ as path to a redoc schema view with the ui and no caching.
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path(settings.ADMIN_URL, admin.site.urls),
]

admin.site.site_header = "Authors Haven API Admin"

admin.site.site_title = "Authors Haven Admin Portal"

admin.site.index_title = "Welcome to Authors Haven API Portal"
