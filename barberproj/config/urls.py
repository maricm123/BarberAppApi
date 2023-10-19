from django.conf import settings
from django.contrib import admin
from django.urls import include, path


app_name="core"


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api.urls", namespace="api")),
]


if settings.DEBUG:
    from rest_framework import urls as rest_urls

    # urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns
    # urlpatterns += [path("__debug__", include(debug_toolbar.urls))]
    # Allow rest_framework login/logout views to test rest APIs
    urlpatterns += [path("", include(rest_urls, namespace="rest_framework"))]