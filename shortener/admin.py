from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Link


class LinkAdmin(ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('short_name', 'full_url', 'created_at')


admin.site.register(Link, LinkAdmin)
