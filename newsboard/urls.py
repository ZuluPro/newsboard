from django.conf.urls import url
from newsboard import views


urlpatterns = [
    url(r'^$', views.StreamListView.as_view(), name='stream-list'),
    url(r'^stream/$', views.StreamListView.as_view(), name='stream-list'),
    url(r'^stream/(?P<slug>[-\w]+)/$', views.StreamDetailView.as_view(), name='stream-detail'),
    url(r'^posts/$', views.PostListView.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>[-\d]+)/$', views.PostDetailView.as_view(), name='post-detail'),
    url(r'^posts/(?P<pk>[-\d]+)/remove/$', views.PostRemoveView.as_view(), name='post-remove'),
]
