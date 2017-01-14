from django.contrib import admin
from .models import Cave

class CaveAdmin(admin.ModelAdmin):
    fields = ['uuid', 'name', 'text', 'author', 'date_created']
    list_display = ['uuid', 'name', 'text', 'author', 'date_created']
    search_fields = ['name', 'author__email']

admin.site.register(Cave, CaveAdmin)
