from django.conf.urls import url
from newsboard import views


urlpatterns = [
    url(r'^$', views.StreamListView.as_view(), name='stream-list'),
    url(r'^posts/$', views.PostListView.as_view(), name='post-list'),
]
