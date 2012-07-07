from django.contrib import admin
from support.models import NeedExpert, NeedHelp


class NeedExpertAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'expert_type', 'ticket_id', 'created']
    raw_id_fields = ['profile']


class NeedHelpAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'ticket_id', 'created']
    raw_id_fields = ['profile']


admin.site.register(NeedExpert, NeedExpertAdmin)
admin.site.register(NeedHelp, NeedHelpAdmin)

