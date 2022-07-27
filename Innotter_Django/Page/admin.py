from django.contrib import admin

from .models import *


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_private')
    search_fields = ('owner', 'name', 'description')
    list_editable = ('is_private',)
    list_filter = ('is_private', 'tags')


admin.site.register(Tag)
admin.site.register(Page, PageAdmin)
