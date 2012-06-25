import json
import urllib
import urllib2


def urllib_request(url, values=None, request_type='GET'):
    if values:
        data = urllib.urlencode(values)
        if request_type == 'GET':
            request = urllib2.Request(url + '?' + data)
        elif request_type == 'POST':
            request = urllib2.Request(url, data)
    else:
        request = urllib2.Request(url)

    response = urllib2.urlopen(request)
    response_json = json.loads(response.read())
    response.close()

    return response_json

