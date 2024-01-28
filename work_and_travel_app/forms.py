from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from work_and_travel_app.models import BaseInformation


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'Invalid username or password',
    }


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        base_info = BaseInformation.objects.create(
            user=user,
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            contact_number=self.cleaned_data['contact_number'],
            date_of_birth=self.cleaned_data['date_of_birth'],
            are_you_traveling=self.cleaned_data['are_you_traveling'],
            country=self.cleaned_data['country'],
            sex=self.cleaned_data['sex']
        )

        if commit:
            user.save()
            base_info.save()

        return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = BaseInformation
        exclude = ['user', 'email']

