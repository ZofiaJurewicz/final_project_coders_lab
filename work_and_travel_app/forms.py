from django import forms

from work_and_travel_app.models import Offer, BaseInformation


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = '__all__'


class EditBaseInfoForm(forms.ModelForm):
    class Meta:
        model = BaseInformation
        exclude = ['user']

