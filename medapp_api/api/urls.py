from django.conf.urls import patterns, include, url
from piston.resource import Resource
from medapp_api.api.handlers import CompareMyPriceHandler


cmp_handler = Resource(CompareMyPriceHandler)


urlpatterns = patterns('',
   url(r'^compare-my-price/', cmp_handler),
)

