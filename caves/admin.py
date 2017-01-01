from django.contrib import admin
from .models import Cave

class CaveAdmin(admin.ModelAdmin):
    fields = ['uuid', 'name', 'text', 'author']
    list_display = ['uuid', 'name', 'text', 'author']
    search_fields = ['name', 'author__email']

admin.site.register(Cave, CaveAdmin)
