"""universe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="BLOGHUB API",
        default_version='v1',
        description="Bloghub description",
        terms_of_service="https://www.bloghub.com/policies/terms/",
        contact=openapi.Contact(email="contact@bloghub.local"),
        license=openapi.License(name="BlogHub License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('blog.urls')),
    path('', include('comment.urls')),
    path('', include('groups.urls')),
    path('', include('profiles.urls')),
    path('', include('pages.urls')),
    path('', include('search.urls')),
    path('home/', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    path('api/api.json/', schema_view.without_ui(cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',cache_timeout=0), name='schema-redoc'),
]
