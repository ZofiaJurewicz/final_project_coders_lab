from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from work_and_travel_app.forms import OfferForm, EditBaseInfoForm
from work_and_travel_app.models import BaseInformation, Offer


class StartView(View):

    def get(self, request):
        return render(request, 'start.html')


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
            return redirect('offers_list_login')

        return render(request, 'add_offer.html', {'form': form})


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
class YourProfile(View):
    def get(self, request):
        user = request.user
        base_info = BaseInformation.objects.filter(user=user).filter()
        if base_info:
            return render(request, 'your_profile.html', {'user': user, 'base_info': base_info})
        else:
            return render(request, 'your_profile.html', {'user': user, 'base_info': None})


@method_decorator(login_required, name='dispatch')
class EditBaseInfoView(View):

    def get(self, request):
        user_info = BaseInformation.objects.get(id=request.user.id)
        form = EditBaseInfoForm(instance=user_info)
        return render(request, 'edit_base_info.html', {'form': form})

    def post(self, request):
        user_info = BaseInformation.objects.get(id=request.user.id)
        form = EditBaseInfoForm(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return redirect('profile')

        return render(request, 'edit_base_info.html', {'form': form})


class OffersListLoginView(View):
    def get(self, request):
        search_country = request.GET.get('search', '')
        offers = Offer.objects.filter(is_active=True)
        if search_country:
            offers = offers.filter(country__icontains=search_country)

        user = request.user if request.user.is_authenticated else None

        ctx = {
            'offers': offers,
            'user': user,
        }

        return render(request, 'offers_list_login.html', ctx)


class OffersListView(View):
    def get(self, request):
        offers = Offer.objects.filter(is_active=True)
        return render(request, 'offers_list.html', {'offers': offers})


@method_decorator(login_required, name='dispatch')
class OfferDetailsLogView(View):

    def get(self, request, name):
        return HttpResponse('')
    #     offer = Offer.objects.get(Offer, name=name)
    #     return render(request, 'offer_details_log.html', {'offer': offer})
    #
    # def post(self, request, name):
    #     pass


class OfferDetailsView(View):
    def get(self, request):
        return render(request, 'offer_details.html')


class EditOfferView(View):
    def get(self, request):
        return render(request, 'edit_offer.html')


class YourOffersCreateView(View):
    def get(self, request):
        return render(request, 'your_offers_create.html')


class YourOffersApplyView(View):
    def get(self, request):
        return render(request, 'your_offers_apply.html')


class MessagesView(View):
    def get(self, request):
        return render(request, 'messages.html')