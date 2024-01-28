from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DetailView

from work_and_travel_app.forms import CustomAuthenticationForm, RegistrationForm, EditProfileForm
from work_and_travel_app.models import BaseInformation


class HomeView(View):

    def get(self, request):
        return render(request, 'home.html')


@method_decorator(csrf_protect, name='dispatch')
class LoginView(View):

    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('profile')
            else:
                form.add_error(None, 'Invalid username or password')
        return render(request, 'login.html', {'form': form})


@method_decorator(csrf_protect, name='dispatch')
class RegisterView(View):

    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('profile')

        return render(request, 'registration.html', {'form': form})


class ProfileView(LoginRequiredMixin, DetailView):
    model = BaseInformation
    template_name = 'your_profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return self.request.user.baseinformation


class EditProfileView(LoginRequiredMixin, View):

    def get(self, request):
        user_info = BaseInformation.objects.get(id=request.user.id)
        form = EditProfileForm(instance=user_info)
        return render(request, 'edit_profile.html', {'form': form})

    def post(self, request):
        user_info = BaseInformation.objects.get(id=request.user.id)
        form = EditProfileForm(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return redirect('profile')

        return render(request, 'edit_profile.html', {'form': form})

