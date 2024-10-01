from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls

if not settings.TESTING:
    urlpatterns = [
                      path("tutorials/", include("tutorial.urls")),
                      path("admin/", admin.site.urls)
                  ] + debug_toolbar_urls()
