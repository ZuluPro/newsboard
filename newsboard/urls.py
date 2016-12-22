from django.conf.urls import url
from newsboard import views


urlpatterns = [
    url(r'^$', views.StreamListView.as_view(), name='stream-list'),
]
