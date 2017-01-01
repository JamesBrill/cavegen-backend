from django.contrib import admin
from .models import Cave

class CaveAdmin(admin.ModelAdmin):
    fields = ['uuid', 'text', 'author']
    list_display = ['uuid', 'text', 'author']
    search_fields = ['author__email']

admin.site.register(Cave, CaveAdmin)
