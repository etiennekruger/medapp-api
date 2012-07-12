import json
import requests
from apns import APNs, Payload
from django.conf import settings
from piston.handler import BaseHandler
from piston.utils import rc, validate
from api.forms import CompareMyPrice2Form, CompareMyPrice3Form,\
    FindSupplier2Form, FindSupplier3Form, PushNotificationForm
from api.utils import get_value
from profile.models import Profile
from profile.forms import GetProfileForm, CreateProfileForm, UpdateProfileForm
from currency.models import Currency
from support.models import NeedExpert, NeedHelp
from support.forms import GetNeedExpertForm, CreateNeedExpertForm,\
    UpdateNeedExpertForm, GetNeedHelpForm, CreateNeedHelpForm, UpdateNeedHelpForm


class ProfileHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')
    model = Profile
    fields = ('id', 'name', 'organisation', 'email', 'phone', 'device_token')

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
        profile.device_token = request.PUT.get('device_token')
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
            if get_value(meddb_item, 'dosageform', 'name') == unit_type:
                result = {}
                result['id'] = get_value(meddb_item, 'id')
                result['dosageform'] = get_value(meddb_item, 'dosageform', 'name')
                result['ingredients'] = []
                for item_ing in meddb_item['ingredients']:
                    result_ing = {}
                    result_ing['inn'] = get_value(item_ing, 'inn')
                    result_ing['strength'] = get_value(item_ing, 'strength')
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
        response['mshprice'] = get_value(meddb_json, 'mshprice')
        response['dosageform'] = get_value(meddb_json, 'dosageform')
        response['results'] = []
        for proc in meddb_json['procurements']:
            result = {}
            result['price'] = get_value(proc, 'price')
            result['country'] = get_value(proc, 'country', 'name')
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
            result['id'] = get_value(meddb_item, 'id')
            result['dosageform'] = get_value(meddb_item, 'dosageform', 'name')
            result['ingredients'] = []
            for item_ing in meddb_item['ingredients']:
                result_ing = {}
                result_ing['inn'] = get_value(item_ing, 'inn')
                result_ing['strength'] = get_value(item_ing, 'strength')
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
        for proc in meddb_json['procurements']:
            if 'supplier' in proc:
                result = {}
                result['name'] = get_value(proc, 'supplier', 'name')
                result['product_name'] = get_value(proc, 'product', 'name')
                result['phone'] = get_value(proc, 'supplier', 'phone')
                result['country'] = get_value(proc, 'supplier', 'manufacturer', 'country', 'name')
                response['results'].append(result)

        return response


"""
class NeedExpertListHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = NeedExpert
    fields = ('id', 'ticket_id')

    @validate(GetNeedExpertListForm, 'GET')
    def read(self, request):
        profile_id = request.GET.get('profile_id')
        need_expert_list = NeedExpert.objects.filter(profile__id=profile_id)
        return need_expert_list
"""


class NeedExpertHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')
    model = NeedExpert
    fields = ('id', 'profile', 'expert_type', 'details', 'ticket_id')

    @validate(GetNeedExpertForm, 'GET')
    def read(self, request):
        ticket_id = request.GET.get('ticket_id')

        url = settings.ZENDESK_URL + '/api/v2/tickets/%s.json' % ticket_id
        auth = (settings.ZENDESK_LOGIN, settings.ZENDESK_PASSWORD)
        response = requests.get(url, auth=auth)
        json = response.json
        if response.status_code != 200:
            return rc.BAD_REQUEST

        return json

    @validate(CreateNeedExpertForm, 'POST')
    def create(self, request):
        profile_id = request.POST.get('profile_id')
        expert_type = request.POST.get('expert_type')
        details = request.POST.get('details')

        try:
            profile = Profile.objects.get(id=profile_id)
        except Exception, e:
            return rc.BAD_REQUEST

        url = settings.ZENDESK_URL + '/api/v2/tickets.json'
        data = {
            'ticket': {
                'subject': 'I need an expert',
                'description': details,
                'assignee_id': 234025206
            }
        }
        headers = {'Content-Type': 'application/json'}
        auth = (settings.ZENDESK_LOGIN, settings.ZENDESK_PASSWORD)
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth)
        ticket_id = response.json['ticket']['id']

        if response.status_code == 201:
            need_expert = NeedExpert.objects.create(profile=profile,
                                                    expert_type=expert_type,
                                                    details=details,
                                                    ticket_id=ticket_id)
            return need_expert
        else:
            return rc.BAD_REQUEST

    @validate(UpdateNeedExpertForm, 'PUT')
    def update(self, request):
        ticket_id = request.GET.get('ticket_id')
        details = request.POST.get('details')

        url = settings.ZENDESK_URL + '/api/v2/tickets/%s.json' % ticket_id
        data = {
            'ticket': {
                'description': details
            }
        }
        headers = {'Content-Type': 'application/json'}
        auth = (settings.ZENDESK_LOGIN, settings.ZENDESK_PASSWORD)
        response = requests.put(url, data=json.dumps(data), headers=headers, auth=auth)
        json = response.json
        if response.status_code != 200:
            return rc.BAD_REQUEST

        return json


"""
class NeedHelpListHandler(BaseHandler):
    allowed_methods = ('GET',)
    model = NeedHelp
    fields = ('id', 'ticket_id')

    @validate(GetNeedHelpListForm, 'GET')
    def read(self, request):
        profile_id = request.GET.get('profile_id')
        need_help_list = NeedHelp.objects.filter(profile__id=profile_id)
        return need_help_list
"""


class NeedHelpHandler(BaseHandler):
    allowed_methods = ('GET', 'POST', 'PUT')
    model = NeedHelp
    fields = ('id', 'profile', 'details', 'ticket_id')

    @validate(GetNeedHelpForm, 'GET')
    def read(self, request):
        ticket_id = request.GET.get('ticket_id')

        url = settings.ZENDESK_URL + '/api/v2/tickets/%s.json' % ticket_id
        auth = (settings.ZENDESK_LOGIN, settings.ZENDESK_PASSWORD)
        response = requests.get(url, auth=auth)
        json = response.json
        if response.status_code != 200:
            return rc.BAD_REQUEST

        return json

    @validate(CreateNeedHelpForm, 'POST')
    def create(self, request):
        profile_id = request.POST.get('profile_id')
        details = request.POST.get('details')

        try:
            profile = Profile.objects.get(id=profile_id)
        except Exception, e:
            return rc.BAD_REQUEST

        url = settings.ZENDESK_URL + '/api/v2/tickets.json'
        data = {
            'ticket': {
                'subject': 'I need help',
                'description': details,
                'assignee_id': 232562443
            }
        }
        headers = {'Content-Type': 'application/json'}
        auth = (settings.ZENDESK_LOGIN, settings.ZENDESK_PASSWORD)
        response = requests.post(url, data=json.dumps(data), headers=headers, auth=auth)
        ticket_id = response.json['ticket']['id']

        if response.status_code == 201:
            need_help = NeedHelp.objects.create(profile=profile,
                                                details=details,
                                                ticket_id=ticket_id)
            return need_help
        else:
            return rc.BAD_REQUEST

    @validate(UpdateNeedHelpForm, 'PUT')
    def update(self, request):
        ticket_id = request.GET.get('ticket_id')
        details = request.POST.get('details')

        url = settings.ZENDESK_URL + '/api/v2/tickets/%s.json' % ticket_id
        data = {
            'ticket': {
                'description': details
            }
        }
        headers = {'Content-Type': 'application/json'}
        auth = (settings.ZENDESK_LOGIN, settings.ZENDESK_PASSWORD)
        response = requests.put(url, data=json.dumps(data), headers=headers, auth=auth)
        json = response.json
        if response.status_code != 200:
            return rc.BAD_REQUEST

        return json


class PushNotificationHandler(BaseHandler):
    allowed_methods = ('GET',)

    @validate(PushNotificationForm, 'GET')
    def read(self, request):
        ticket_id = request.GET.get('ticket_id')
        message = request.GET.get('message')
        device_token = None

        for need in (NeedExpert, NeedHelp):
            try:
                ticket = need.objects.get(ticket_id=ticket_id)
                device_token = ticket.profile.device_token
                break
            except:
                pass
        if device_token is None:
            return rc.NOT_FOUND

        apns = APNs(use_sandbox=True, cert_file=settings.CERT_FILE)
        payload = Payload(alert=message)
        result = apns.gateway_server.send_notification(device_token, payload)
        return {'result': result}

