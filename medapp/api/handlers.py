import json
import requests
from django.conf import settings
from piston.handler import BaseHandler
from piston.utils import rc, validate
from api.forms import CompareMyPrice2Form, CompareMyPrice3Form,\
    FindSupplier2Form, FindSupplier3Form
from profile.models import Profile
from profile.forms import GetProfileForm, CreateProfileForm, UpdateProfileForm
from currency.models import Currency
from support.models import NeedExpert, NeedHelp
from support.forms import NeedExpertForm, NeedHelpForm


class ProfileHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')
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

    @validate(CreateProfileForm, 'POST')
    def create(self, request):
        payload = self.flatten_dict(request.POST)
        profile = self.model.objects.create(**payload)
        return profile

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

        try:
            currency_rate = Currency.objects.get(name=currency).rate
        except Exception, e:
            return rc.BAD_REQUEST

        url = settings.MEDDB_URL + '/json/medicine/'
        params = {'search': med_name}
        meddb_response = requests.get(url, params=params)
        meddb_json = meddb_response.json
        if meddb_response.status_code != 200:
            return rc.BAD_REQUEST

        response = {}
        response['my_price'] = currency_rate * price / num_unit
        response['results'] = []
        for meddb_item in meddb_json:
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

        url = settings.MEDDB_URL + '/json/medicine/%s/' % med_id
        meddb_response = requests.get(url)
        meddb_json = meddb_response.json
        if meddb_response.status_code != 200:
            return rc.BAD_REQUEST

        response = {}
        response['mshprice'] = meddb_json['mshprice']
        response['dosageform'] = meddb_json['dosageform']
        response['results'] = []
        for procurement in meddb_json['procurements']:
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

        url = settings.MEDDB_URL + '/json/medicine/'
        params = {'search': med_name}
        meddb_response = requests.get(url, params=params)
        meddb_json = meddb_response.json
        if meddb_response.status_code != 200:
            return rc.BAD_REQUEST

        response = {}
        response['results'] = []
        for meddb_item in meddb_json:
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

        url = settings.MEDDB_URL + '/json/medicine/%s/' % med_id
        meddb_response = requests.get(url)
        meddb_json = meddb_response.json
        if meddb_response.status_code != 200:
            return rc.BAD_REQUEST

        response = {}
        response['results'] = []
        for procurement in meddb_json['procurements']:
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

        url = settings.ZENDESK_URL + '/api/v2/tickets.json'
        data = {'ticket': {'subject': 'I need an expert', 'description': details}}
        headers = {'Content-Type': 'application/json'}
        auth = (settings.ZENDESK_LOGIN, settings.ZENDESK_PASSWORD)
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth)

        if response.status_code == 201:
            need_expert = NeedExpert.objects.create(profile=profile,
                                                    expert_type=expert_type,
                                                    details=details)
            return need_expert
        else:
            return rc.BAD_REQUEST


class NeedHelpHandler(BaseHandler):
    allowed_methods = ('POST',)
    model = NeedHelp
    fields = ('id', 'profile', 'details')

    @validate(NeedHelpForm, 'POST')
    def create(self, request):
        profile_id = request.POST.get('profile_id')
        details = request.POST.get('details')

        try:
            profile = Profile.objects.get(id=profile_id)
        except Exception, e:
            return rc.BAD_REQUEST

        url = settings.ZENDESK_URL + '/api/v2/tickets.json'
        data = {'ticket': {'subject': 'I need help', 'description': details}}
        headers = {'Content-Type': 'application/json'}
        auth = (settings.ZENDESK_LOGIN, settings.ZENDESK_PASSWORD)
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth)

        if response.status_code == 201:
            need_help = NeedHelp.objects.create(profile=profile, details=details)
            return need_help
        else:
            return rc.BAD_REQUEST

