from django.contrib import admin
from newsboard import urls

try:
    from django.conf.urls import patterns, include, url
    urlpatterns = patterns(
        '',
        url(r'^', include(urls.urlpatterns)),
        url(r'^admin/', include(admin.site.urls)),
    )
except ImportError:
    from django.conf.urls import include, url
    urlpatterns = (
        url(r'^', include(urls.urlpatterns)),
        url(r'^admin/', include(admin.site.urls)),
    )
