from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from work_and_travel_app.forms import OfferForm, EditBaseInfoForm
from work_and_travel_app.models import BaseInformation


@method_decorator(login_required, name='dispatch')
class AddOfferView(View):
    def get(self, request):
        form = OfferForm()
        return render(request, 'add_offer.html', {'form': form})

    def post(self, request):
        form = OfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.owner = request.user
            offer.save()
            return redirect('your_offers_list')

        return render(request, 'add_offer.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class YourProfile(View):
    def get(self, request):
        user = request.user
        base_info = BaseInformation.objects.filter(user=user).filter()
        if base_info:
            return render(request, 'your_profile.html', {'user': user, 'base_info': base_info})
        else:
            return redirect('add_base_info')


@method_decorator(login_required, name='dispatch')
class AddBaseInfoView(View):

    def get(self, request):
        form = EditBaseInfoForm()
        return render(request, 'add_base_info.html', {'form': form})

    def post(self, request):
        form = EditBaseInfoForm(request.POST)

        if form.is_valid():
            base_info = form.save(commit=False)
            base_info.user = request.user
            base_info.save()
            return redirect('your_profile')

        return render(request, 'add_base_info.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditBaseInfoView(View):

    def get(self, request):
        user = request.user
        base_info = BaseInformation.objects.get(user=user)
        form = self.EditBaseInfoForm(isinstance=base_info)
        return render(request, 'edit_base_info.html', {'form': form})

    def post(self, request):
        user = request.user
        base_info = BaseInformation.objects.get(user=user)
        form = self.EditBaseInfoForm(request.POST, isinstance=base_info)

        if form.is_valid:
            form.save()
            return redirect('your_profile')

        return render(request, 'edit_base_info.html', {'form': form})

