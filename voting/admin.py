#-*- coding: utf-8 -*-
from django.contrib import admin

from .models import Aspirant, Office


class AspirantInline(admin.TabularInline):
    model = Aspirant
    readonly_fields = ('votes',)
    extra = 3


class OfficeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['office'],
        }),
    ]
    inlines = [AspirantInline]
    list_display = ('office',)
    search_fields = ['office']

admin.site.register(Office, OfficeAdmin)
admin.site.register(Aspirant)
