from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.views import generic
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from newsboard import models
from newsboard import tasks


class ContextMxinView(generic.base.ContextMixin):
    def get_context_data(self, **kwargs):
        context = super(ContextMxinView, self).get_context_data(**kwargs)
        context['title'] = self.title
        return context


class StreamListView(ContextMxinView, generic.list.ListView):
    model = models.Stream
    template_name = 'newsboard/streams.html'
    title = model._meta.verbose_name_plural.capitalize()

    def get_queryset(self):
        return self.model.objects.all()

    def post(self, request):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        stream_ids = request.POST.getlist('stream_id')
        if request.POST.get('mode', 'async') == 'async':
            messages.info(request, _("Stream(s) updating in progess."))
            tasks.update_streams.delay(stream_ids)
        else:
            for stream_id in stream_ids:
                tasks.update_stream(stream_id)
            messages.info(request, _("Stream(s) updating finished."))
        return redirect('stream-list')


class StreamDetailView(generic.detail.DetailView, ContextMxinView):
    model = models.Stream
    template_name = 'newsboard/stream.html'

    @property
    def title(self):
        return self.get_object().name

    def post(self, request, slug):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        stream = self.get_object()
        if request.POST.get('mode', 'async') == 'async':
            tasks.update_stream.delay(stream.id)
            messages.info(request, _("Stream updating in progess."))
        else:
            tasks.update_stream(stream.id)
            messages.info(request, _("Stream updating finished."))
        return redirect(stream.get_absolute_url())


class PostListView(generic.list.ListView, ContextMxinView):
    model = models.Post
    template_name = 'newsboard/posts.html'
    title = model._meta.verbose_name_plural.capitalize()

    def get_queryset(self):
        return self.model.objects\
            .filter(is_removed=False)\
            .order_by('-updated_at')

    def post(self, request):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        if request.POST.get('mode', 'async') == 'async':
            tasks.update_all_streams.delay()
            messages.info(request, _("Stream updating in progess."))
        else:
            for stream in models.Stream.objects.filter(auto_enabled=True):
                stream.update_posts()
            messages.info(request, _("Stream updating finished."))
        return redirect('post-list')


class PostDetailView(generic.detail.DetailView, ContextMxinView):
    model = models.Post
    template_name = 'newsboard/post.html'

    @property
    def title(self):
        return self.get_object().name


class PostRemoveView(generic.View):
    model = models.Post

    def post(self, request, pk):
        if not request.user.is_staff:
            return HttpResponseForbidden()
        post = get_object_or_404(self.model.objects.filter(id=pk, is_removed=False))
        post.is_removed = True
        post.save()
        messages.info(request, _("Post has been removed."))
        next_ = request.POST.get('next', 'stream-list')
        return redirect(next_)
