from piston.handler import BaseHandler


class CompareMyPriceHandler(BaseHandler):
    allowed_methods = ('GET',)

    def read(self, request):
        json = {'first_name': 'Andrey', 'last_name': 'Makhonin'}
        return json

