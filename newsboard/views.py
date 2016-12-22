from django.shortcuts import render
from django.views.generic.list import ListView
from newsboard import models


class StreamListView(ListView):
    model = models.Stream
    template_name = 'newsboard/streams.html'

    def get_queryset(self):
        return self.model.objects.all()


class PostListView(ListView):
    model = models.Post
    template_name = 'newsboard/posts.html'

    def get_queryset(self):
        return self.model.objects.order_by('-updated_at')
