import json
import urllib
import urllib2
from piston.handler import BaseHandler


class CompareMyPriceHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, unit_id=None):
        if unit_id:
            url = 'http://meddb.medicinesinfohub.net/json/medicine/%s/' % unit_id
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            response_json = json.loads(response.read())
            response.close()

            results = response_json
        else:
            search = request.GET.get('search')
            unit_type = request.GET.get('unit_type')
            url = 'http://meddb.medicinesinfohub.net/json/medicine/'
            values = {'search': search}
            data = urllib.urlencode(values)
            request = urllib2.Request(url + '?' + data)
            response = urllib2.urlopen(request)
            response_json = json.loads(response.read())
            response.close()

            results = []
            for response_item in response_json:
                if response_item['dosageform']['name'] == unit_type:
                    results.append(response_item)

        return results


class FindSupplierHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, unit_id=None):
        if unit_id:
            url = 'http://meddb.medicinesinfohub.net/json/medicine/%s/' % unit_id
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            response_json = json.loads(response.read())
            response.close()
        else:
            search = request.GET.get('search')
            url = 'http://meddb.medicinesinfohub.net/json/medicine/'
            values = {'search': search}
            data = urllib.urlencode(values)
            request = urllib2.Request(url + '?' + data)
            response = urllib2.urlopen(request)
            response_json = json.loads(response.read())
            response.close()

        return response_json

