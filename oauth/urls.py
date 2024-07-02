"""
URL configuration for oauth project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

from users.views import (
    ApproveAuthorizationView,
    DenyAuthorizationView,
    RequestAuthorizationView,
)
from oauth2_provider import views

# from users.views import ApiEndpoint

urlpatterns = [
    path("admin/", admin.site.urls),
    # path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path(
        "o/request",
        RequestAuthorizationView.as_view(),
        name="request_authorization",
    ),
    path(
        "o/approve",
        ApproveAuthorizationView.as_view(),
        name="approve_authorization",
    ),
    path(
        "o/deny",
        DenyAuthorizationView.as_view(),
        name="deny_authorization",
    ),
    path(
        "api/v1/",
        include(
            [path("users/", include("users.urls"))],
        ),
    ),
]
