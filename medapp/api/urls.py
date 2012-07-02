from django.conf.urls import patterns, include, url
from piston.resource import Resource
from api.handlers import RegistrationHandler, GetProfileHandler,\
    UpdateProfileHandler, CompareMyPrice2Handler, CompareMyPrice3Handler,\
    FindSupplier2Handler, FindSupplier3Handler, NeedExpertHandler, NeedHelpHandler


reg_handler = Resource(RegistrationHandler)
get_handler = Resource(GetProfileHandler)
upd_handler = Resource(UpdateProfileHandler)

cmp2_handler = Resource(CompareMyPrice2Handler)
cmp3_handler = Resource(CompareMyPrice3Handler)

fs2_handler = Resource(FindSupplier2Handler)
fs3_handler = Resource(FindSupplier3Handler)

ne_handler = Resource(NeedExpertHandler)
nh_handler = Resource(NeedHelpHandler)


urlpatterns = patterns('',
    url(r'^registration/$', reg_handler),
    url(r'^get-profile/$', get_handler),
    url(r'^update-profile/$', upd_handler),

    url(r'^compare-my-price/2/$', cmp2_handler),
    url(r'^compare-my-price/3/$', cmp3_handler),

    url(r'^find-supplier/2/$', fs2_handler),
    url(r'^find-supplier/3/$', fs3_handler),

    url(r'^need-expert/$', ne_handler),
    url(r'^need-help/$', nh_handler),
)

