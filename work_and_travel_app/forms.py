from django import forms

from work_and_travel_app.models import Offer, BaseInformation, Message


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ['owner']


class AddBaseInfoForm(forms.ModelForm):
    class Meta:
        model = BaseInformation
        exclude = ['user']


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'placehlder': 'Write a message...'})
        }

