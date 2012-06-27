from django.contrib import admin
from currency.models import Currency


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'rate', 'updated']


admin.site.register(Currency, CurrencyAdmin)

