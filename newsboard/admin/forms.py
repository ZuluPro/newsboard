from django import forms
from dj_web_rich_object.admin import forms as wro_forms
from newsboard import models


class PostAdminForm(wro_forms.WebRichObjectAdminForm):
    class Meta(wro_forms.WebRichObjectAdminForm.Meta):
        model = models.Post


class PostAdminAddForm(forms.ModelForm):
    class Meta(PostAdminForm):
        fields = ('url', 'streams')
