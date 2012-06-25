from piston.handler import BaseHandler
from piston.utils import validate
from profile.models import Profile
from profile.forms import ProfileForm
from utils.urllibs import urllib_request


class RegistrationHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Profile
    fields = ('id',)

    @validate(ProfileForm, 'POST')
    def create(self, request):
        payload = self.flatten_dict(request.POST)
        profile = self.model.objects.create(**payload)
        return profile


class CompareMyPriceHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, unit_id=None):
        if unit_id:
            url = 'http://meddb.medicinesinfohub.net/json/medicine/%s/' % unit_id
            result = urllib_request(url)
        else:
            search = request.GET.get('search')
            unit_type = request.GET.get('unit_type')
            url = 'http://meddb.medicinesinfohub.net/json/medicine/'
            values = {'search': search}
            response = urllib_request(url, values)

            result = []
            for item in response:
                if item['dosageform']['name'] == unit_type:
                    result.append(item)

        return result


class FindSupplierHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request, unit_id=None):
        if unit_id:
            url = 'http://meddb.medicinesinfohub.net/json/medicine/%s/' % unit_id
            result = urllib_request(url)
        else:
            search = request.GET.get('search')
            url = 'http://meddb.medicinesinfohub.net/json/medicine/'
            values = {'search': search}
            result = urllib_request(url, values)

        return result

