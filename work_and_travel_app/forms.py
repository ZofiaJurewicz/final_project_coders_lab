from django.utils import timezone

from django import forms
from django.core.exceptions import ValidationError

from work_and_travel_app.models import Offer, BaseInformation, Message, Grade, Answer


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ['owner']

    def clean(self, ):
        cleaned_data = super().clean()
        since_when = self.cleaned_data["since_when"]
        until_when = self.cleaned_data["until_when"]
        today = timezone.now().date()

        if since_when < today:
            raise ValidationError('None of the dates can be older than today.')
        elif until_when < today:
            raise ValidationError('None of the dates can be older than today')

        if until_when:
            if until_when < since_when:
                raise ValidationError('"Since when" date must be later than the "until when" date.')


class AddBaseInfoForm(forms.ModelForm):
    class Meta:
        model = BaseInformation
        exclude = ['user']

    def clean_date_of_birth(self):
        cleaned_data = super().clean()
        date_of_birth = self.cleaned_data['date_of_birth']
        if date_of_birth > timezone.now().date():
            raise ValidationError("The given date of birth is in the future.")

        return date_of_birth


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        exclude = ['user', 'message']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'grade_answer']
