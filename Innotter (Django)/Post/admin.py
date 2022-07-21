from django.contrib import admin

from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'page', 'reply_to', 'created_at')
    search_fields = ('page', 'content')
    list_filter = ('page', 'created_at', 'updated_at')


admin.site.register(Post, PostAdmin)
