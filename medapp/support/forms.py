from django import forms
from support.models import NeedExpert, NeedHelp


class NeedExpertForm(forms.Form):
    profile_id = forms.IntegerField()
    expert_type = forms.CharField(max_length=255)
    details = forms.CharField(max_length=255)


class NeedHelpForm(forms.Form):
    profile_id = forms.IntegerField()
    details = forms.CharField(max_length=255)

