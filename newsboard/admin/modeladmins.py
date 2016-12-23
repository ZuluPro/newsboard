from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from dj_web_rich_object.admin.modeladmins import WebRichObjectAdmin
from newsboard import tasks


class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'remote_id', 'last_updated', 'auto_enabled', 'auto_frequency')
    list_filter = ('type', 'auto_enabled')
    actions = ('update', 'enable_auto', 'disable_auto')
    prepopulated_fields = {'slug': ('name', )}

    def update(self, request, queryset):
        stream_ids = list(queryset.values_list('id', flat=True))
        tasks.update_streams.delay(stream_ids)
    update.short_description = _("Update selected streams")

    def enable_auto(self, request, queryset):
        queryset.update(auto_enabled=True)
    enable_auto.short_description = _("Enable automatic updating")

    def disable_auto(self, request, queryset):
        queryset.update(auto_enabled=False)
    disable_auto.short_description = _("Disable automatic updating")


class PostAdmin(WebRichObjectAdmin):
    actions = WebRichObjectAdmin.actions + ('remove_posts', 'unremove_posts')
    list_display = WebRichObjectAdmin.list_display + ('is_removed',)
    list_filter = WebRichObjectAdmin.list_filter + ('streams', 'is_removed')

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(WebRichObjectAdmin, self).get_fieldsets(request, obj)
        if obj is not None and ('streams', 'is_removed') not in fieldsets[0][1]['fields']:
            fieldset = (('streams', 'is_removed'),) + fieldsets[0][1]['fields']
            fieldsets[0][1]['fields'] = fieldset
        return fieldsets

    def remove_posts(self, request, queryset):
        queryset.update(is_removed=True)
    remove_posts.short_description = _("Remove selected posts")

    def unremove_posts(self, request, queryset):
        queryset.update(is_removed=False)
    unremove_posts.short_description = _("Display selected posts")
