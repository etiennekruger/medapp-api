from piston.handler import BaseHandler
from piston.utils import rc, validate
from api.forms import CompareMyPrice2Form, CompareMyPrice3Form,\
    FindSupplier2Form, FindSupplier3Form
from profile.models import Profile
from profile.forms import RegistrationForm, GetProfileForm, UpdateProfileForm
from currency.models import Currency
from support.models import NeedExpert, NeedHelp
from support.forms import NeedExpertForm, NeedHelpForm
from utils.urllibs import urllib_request


class RegistrationHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = Profile
    fields = ('id', 'name', 'organisation', 'email', 'phone')

    @validate(RegistrationForm, 'POST')
    def create(self, request):
        payload = self.flatten_dict(request.POST)
        profile = self.model.objects.create(**payload)
        return profile


class GetProfileHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = Profile
    fields = ('id', 'name', 'organisation', 'email', 'phone')

    @validate(GetProfileForm, 'GET')
    def read(self, request):
        profile_id = request.GET.get('profile_id')

        try:
            profile = Profile.objects.get(id=profile_id)
        except Exception, e:
            return rc.NOT_FOUND
        return profile


class UpdateProfileHandler(BaseHandler):
    allowed_methods = ('PUT',)
    model = Profile
    fields = ('id', 'name', 'organisation', 'email', 'phone')

    @validate(UpdateProfileForm, 'PUT')
    def update(self, request):
        profile_id = request.PUT.get('profile_id')

        try:
            profile = Profile.objects.get(id=profile_id)
        except Exception, e:
            return rc.NOT_FOUND

        profile.name = request.PUT.get('name')
        profile.organisation = request.PUT.get('organisation')
        profile.email = request.PUT.get('email')
        profile.phone = request.PUT.get('phone')
        profile.save()

        return profile


class CompareMyPrice2Handler(BaseHandler):
    allowed_methods = ('GET',)

    @validate(CompareMyPrice2Form, 'GET')
    def read(self, request):
        med_name = request.GET.get('med_name')
        price = float(request.GET.get('price'))
        currency = request.GET.get('currency')
        unit_type = request.GET.get('unit_type')
        num_unit = float(request.GET.get('num_unit'))

        url = 'http://meddb.medicinesinfohub.net/json/medicine/'
        values = {'search': med_name}
        meddb_response = urllib_request(url, values)
        if meddb_response == 'Invalid request':
            return rc.BAD_REQUEST

        try:
            currency_rate = Currency.objects.get(name=currency).rate
        except Exception, e:
            return rc.BAD_REQUEST

        response = {}
        response['my_price'] = currency_rate * price / num_unit
        response['results'] = []
        for meddb_item in meddb_response:
            if meddb_item['dosageform']['name'] == unit_type:
                result = {}
                result['id'] = meddb_item['id']
                result['dosageform'] = meddb_item['dosageform']['name']
                result['ingredients'] = []
                for item_ing in meddb_item['ingredients']:
                    result_ing = {}
                    result_ing['inn'] = item_ing['inn']
                    result_ing['strength'] = item_ing['strength']
                    result['ingredients'].append(result_ing)
                response['results'].append(result)

        return response


class CompareMyPrice3Handler(BaseHandler):
    allowed_methods = ('GET',)

    @validate(CompareMyPrice3Form, 'GET')
    def read(self, request):
        med_id = request.GET.get('med_id')

        url = 'http://meddb.medicinesinfohub.net/json/medicine/%s/' % med_id
        meddb_response = urllib_request(url)
        if meddb_response == 'Invalid request':
            return rc.BAD_REQUEST

        response = {}
        response['mshprice'] = meddb_response['mshprice']
        response['dosageform'] = meddb_response['dosageform']
        response['results'] = []
        for procurement in meddb_response['procurements']:
            result = {}
            result['price'] = procurement['price']
            result['country'] = procurement['country']['name']
            response['results'].append(result)

        return response


class FindSupplier2Handler(BaseHandler):
    allowed_methods = ('GET',)

    @validate(FindSupplier2Form, 'GET')
    def read(self, request):
        med_name = request.GET.get('med_name')

        url = 'http://meddb.medicinesinfohub.net/json/medicine/'
        values = {'search': med_name}
        meddb_response = urllib_request(url, values)
        if meddb_response == 'Invalid request':
            return rc.BAD_REQUEST

        response = {}
        response['results'] = []
        for meddb_item in meddb_response:
            result = {}
            result['id'] = meddb_item['id']
            result['dosageform'] = meddb_item['dosageform']['name']
            result['ingredients'] = []
            for item_ing in meddb_item['ingredients']:
                result_ing = {}
                result_ing['inn'] = item_ing['inn']
                result_ing['strength'] = item_ing['strength']
                result['ingredients'].append(result_ing)
            response['results'].append(result)

        return response


class FindSupplier3Handler(BaseHandler):
    allowed_methods = ('GET',)

    @validate(FindSupplier3Form, 'GET')
    def read(self, request):
        med_id = request.GET.get('med_id')

        url = 'http://meddb.medicinesinfohub.net/json/medicine/%s/' % med_id
        meddb_response = urllib_request(url)
        if meddb_response == 'Invalid request':
            return rc.BAD_REQUEST

        response = {}
        response['results'] = []
        for procurement in meddb_response['procurements']:
            result = {}
            result['name'] = procurement['supplier']['name']
            result['product_name'] = procurement['product']['name']
            result['country'] = procurement['supplier']['country']['name']
            result['phone'] = procurement['supplier']['phone']
            response['results'].append(result)

        return response


class NeedExpertHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = NeedExpert
    fields = ('id', 'profile', 'expert_type', 'details')

    @validate(NeedExpertForm, 'POST')
    def create(self, request):
        profile_id = request.POST.get('profile_id')
        expert_type = request.POST.get('expert_type')
        details = request.POST.get('details')

        try:
            profile = Profile.objects.get(id=profile_id)
        except Exception, e:
            return rc.BAD_REQUEST

        need_expert = NeedExpert.objects.create(profile=profile,
                                                expert_type=expert_type,
                                                details=details)

        return need_expert


class NeedHelpHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = NeedHelp
    fields = ('id', 'profile', 'details')

    @validate(NeedHelpForm, 'GET')
    def read(self, request):
        profile_id = request.GET.get('profile_id')
        details = request.GET.get('details')

        url = 'https://teststeelkiwi.zendesk.com/api/v2/tickets.json'
        values = {'ticket': {'subject': 'I need help!!!', 'description': 'Description'}}
        zendesk_response = urllib_request(url, values, 'POST')
        if zendesk_response == 'Invalid request':
            return rc.BAD_REQUEST

        try:
            profile = Profile.objects.get(id=profile_id)
        except Exception, e:
            return rc.BAD_REQUEST

        need_help = NeedHelp.objects.create(profile=profile, details=details)

        return need_help

