from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'picture', 'display_name']
    list_display = ['user', 'picture', 'display_name']
    search_fields = ['user__name', 'user__email', 'display_name']


admin.site.register(UserProfile, UserProfileAdmin)
