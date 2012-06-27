from django.conf.urls import patterns, include, url
from piston.resource import Resource
from api.handlers import RegistrationHandler, CompareMyPrice2Handler,\
    CompareMyPrice3Handler, FindSupplier2Handler, FindSupplier3Handler


reg_handler = Resource(RegistrationHandler)

cmp2_handler = Resource(CompareMyPrice2Handler)
cmp3_handler = Resource(CompareMyPrice3Handler)

fs2_handler = Resource(FindSupplier2Handler)
fs3_handler = Resource(FindSupplier3Handler)


urlpatterns = patterns('',
    url(r'^registration/$', reg_handler),

    url(r'^compare-my-price2/$', cmp2_handler),
    url(r'^compare-my-price3/$', cmp3_handler),

    url(r'^find-supplier2/$', fs2_handler),
    url(r'^find-supplier3/$', fs3_handler),
)

