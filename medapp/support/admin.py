from django.contrib import admin
from support.models import NeedExpert, NeedHelp


class NeedExpertAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'created']
    raw_id_fields = ['profile']


class NeedHelpAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'created']
    raw_id_fields = ['profile']


admin.site.register(NeedExpert, NeedExpertAdmin)
admin.site.register(NeedHelp, NeedHelpAdmin)

