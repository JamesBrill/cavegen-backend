from django.contrib import admin
from .models import UserProfile
from caves.models import Cave


class CaveInline(admin.TabularInline):
    model = UserProfile.liked_caves.through


class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'picture', 'display_name', 'liked_caves']
    list_display = ['user', 'picture', 'display_name']
    search_fields = ['user__name', 'user__email', 'display_name']
    inlines = [CaveInline, ]


admin.site.register(UserProfile, UserProfileAdmin)
