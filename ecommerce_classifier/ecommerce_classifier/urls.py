"""ecommerce_classifier URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from main.views import home

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Text Categorizer",
      default_version='v1',
      description="Text Categorizer",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

from main.views import get_cateogry, search, filter_by_category, filter_by_sub_category, filter_by_brand

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home),
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('categorize', get_cateogry),
    path('search', search),
    path('filter-by-category/<category_slug>', filter_by_category),
    path('filter-by-sub-category/<sub_category_slug>', filter_by_sub_category),
    path('filter-by-brand/<brand>', filter_by_brand),
]
