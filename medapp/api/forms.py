from django import forms


class CompareMyPrice2Form(forms.Form):
    med_name = forms.CharField(max_length=255)
    type_price = forms.CharField(max_length=255, required=False)
    price = forms.FloatField(required=False)
    currency = forms.CharField(max_length=255, required=False)
    unit_type = forms.CharField(max_length=255, required=False)
    num_unit = forms.FloatField(required=False)


class CompareMyPrice3Form(forms.Form):
    med_id = forms.IntegerField()


class FindSupplier2Form(forms.Form):
    med_name = forms.CharField(max_length=255)


class FindSupplier3Form(forms.Form):
    med_id = forms.IntegerField()


class PushNotificationForm(forms.Form):
    ticket_id = forms.IntegerField()
    message = forms.CharField(max_length=255)

