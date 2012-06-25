from django.conf.urls import patterns, include, url
from piston.resource import Resource
from api.handlers import RegistrationHandler, CompareMyPriceHandler, FindSupplierHandler


reg_handler = Resource(RegistrationHandler)
cmp_handler = Resource(CompareMyPriceHandler)
fs_handler = Resource(FindSupplierHandler)


urlpatterns = patterns('',
    url(r'^registration/$', reg_handler),

    url(r'^compare-my-price/$', cmp_handler),
    url(r'^compare-my-price/(?P<unit_id>\d+)/$', cmp_handler),

    url(r'^find-supplier/$', fs_handler),
    url(r'^find-supplier/(?P<unit_id>\d+)/$', fs_handler),
)

