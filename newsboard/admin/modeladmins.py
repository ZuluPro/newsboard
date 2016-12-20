from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from dj_web_rich_object.admin.modeladmins import WebRichObjectAdmin
from newsboard import tasks


class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'remote_id')
    list_filter = ('type',)
    actions = ('update',)

    def update(self, request, queryset):
        stream_ids = list(queryset.values_list('id', flat=True))
        tasks.update_streams.delay(stream_ids)
    update.short_description = _("Update selected streams")


class PostAdmin(WebRichObjectAdmin):
    list_display = WebRichObjectAdmin.list_display
    list_filter = WebRichObjectAdmin.list_filter + ('streams',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(WebRichObjectAdmin, self).get_fieldsets(request, obj)
        if obj is not None and 'streams' not in fieldsets[0][1]['fields']:
            fieldset = ('streams',) + fieldsets[0][1]['fields']
            fieldsets[0][1]['fields'] = fieldset
        return fieldsets
