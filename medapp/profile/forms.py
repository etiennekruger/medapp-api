from django import forms
from profile.models import Profile


class GetProfileForm(forms.Form):
    profile_id = forms.IntegerField()


class CreateProfileForm(forms.ModelForm):

    class Meta:
        model = Profile


class UpdateProfileForm(forms.ModelForm):
    profile_id = forms.IntegerField()

    class Meta:
        model = Profile

