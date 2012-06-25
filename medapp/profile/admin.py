from django.contrib import admin
from profile.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'created', 'updated']


admin.site.register(Profile, ProfileAdmin)

