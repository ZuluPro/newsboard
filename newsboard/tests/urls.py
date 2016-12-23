from django.contrib import admin
from newsboard import urls

try:
    from django.conf.urls import patterns, include, url
    urlpatterns = patterns(
        '',
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include(urls.urlpatterns)),
    )
except ImportError:
    from django.conf.urls import include, url
    urlpatterns = (
        url(r'^admin/', include(admin.site.urls)),
        url(r'^', include(urls.urlpatterns)),
    )
