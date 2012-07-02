from django import forms


class CompareMyPrice2Form(forms.Form):
    med_name = forms.CharField(max_length=255)
    type_price = forms.CharField(max_length=255, required=False)
    price = forms.FloatField()
    currency = forms.CharField(max_length=255)
    unit_type = forms.CharField(max_length=255)
    num_unit = forms.FloatField()


class CompareMyPrice3Form(forms.Form):
    med_id = forms.IntegerField()
    my_price = forms.FloatField()


class FindSupplier2Form(forms.Form):
    med_name = forms.CharField(max_length=255)


class FindSupplier3Form(forms.Form):
    med_id = forms.IntegerField()

