from django import forms
from support.models import NeedExpert, NeedHelp


class GetNeedExpertListForm(forms.Form):
    profile_id = forms.IntegerField()


class GetNeedExpertForm(forms.Form):
    ticket_id = forms.IntegerField()


class CreateNeedExpertForm(forms.Form):
    profile_id = forms.IntegerField()
    expert_type = forms.CharField(max_length=255)
    details = forms.CharField(max_length=255)


class UpdateNeedExpertForm(forms.Form):
    ticket_id = forms.IntegerField()
    details = forms.CharField(max_length=255)


class GetNeedHelpListForm(forms.Form):
    profile_id = forms.IntegerField()


class GetNeedHelpForm(forms.Form):
    ticket_id = forms.IntegerField()


class CreateNeedHelpForm(forms.Form):
    profile_id = forms.IntegerField()
    details = forms.CharField(max_length=255)


class UpdateNeedHelpForm(forms.Form):
    ticket_id = forms.IntegerField()
    details = forms.CharField(max_length=255)

