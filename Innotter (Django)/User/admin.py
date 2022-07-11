from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('username','email', 'role', 'is_blocked')
    search_fields = ('email', 'username')
    list_editable = ('is_blocked',)
    list_filter = ('role',)


admin.site.register(User, UserAdmin)
