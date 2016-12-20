from django.contrib import admin
from newsboard.admin import modeladmins
from newsboard import models


admin.site.register(models.Stream, modeladmins.StreamAdmin)
admin.site.register(models.Post, modeladmins.PostAdmin)
