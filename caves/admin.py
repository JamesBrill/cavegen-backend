from django.contrib import admin
from .models import Cave


class CaveAdmin(admin.ModelAdmin):
    fields = ['uuid', 'name', 'text', 'author', 'date_created', 'likes']
    list_display = ['uuid', 'name', 'text', 'author', 'date_created', 'get_author_name', 'likes']
    readonly_fields = ('date_created',)
    search_fields = ['name', 'author__email']

    def get_author_name(self, obj):
        return obj.author.userprofile.display_name
    get_author_name.admin_order_field = 'author'  # Allows column order sorting
    get_author_name.short_description = 'Author Name'  # Renames column head

admin.site.register(Cave, CaveAdmin)
