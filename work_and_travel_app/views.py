from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View

from work_and_travel_app.forms import OfferForm, AddBaseInfoForm, MessageForm
from work_and_travel_app.models import BaseInformation, Offer, Message


class StartView(View):

    def get(self, request):
        search_country = request.GET.get('search', '')
        offers = Offer.objects.filter(is_active=True)

        if search_country:
            offers = offers.filter(country__icontains=search_country)
            return render(request, 'offers_list.html', {'offers': offers})

        return render(request, 'start.html')


class YourProfile(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('start')
        user = request.user
        base_info = BaseInformation.objects.filter(user=user).filter()
        if base_info:
            return render(request, 'your_profile.html', {'user': user, 'base_info': base_info})
        else:
            return render(request, 'your_profile.html', {'user': user, 'base_info': None})


@method_decorator(login_required, name='dispatch')
class AddBaseInfoView(View):

    def get(self, request):
        form = AddBaseInfoForm()
        return render(request, 'add_base_info.html', {'form': form})

    def post(self, request):
        form = AddBaseInfoForm(request.POST)

        if form.is_valid():
            base_info = form.save(commit=False)
            base_info.user = request.user
            base_info.save()
            return redirect('your_profile')

        return render(request, 'add_base_info.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditBaseInfoView(View):

    def get(self, request):
        user_info = BaseInformation.objects.filter(user=request.user).first()
        form = AddBaseInfoForm(instance=user_info)
        return render(request, 'edit_base_info.html', {'form': form})

    def post(self, request):
        user_info = BaseInformation.objects.filter(user=request.user).first()
        form = AddBaseInfoForm(request.POST, instance=user_info)
        if form.is_valid():
            form.save()
            return redirect('your_profile')

        return render(request, 'edit_base_info.html', {'form': form})


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
            return redirect('offers_list')

        return render(request, 'add_offer.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class EditOfferView(View):

    def get(self, request, offer_id):
        offer_info = get_object_or_404(Offer, id=offer_id)
        if offer_info.user != request.user:
            raise Http404("You don't have permission to edit this offer.")
        form = OfferForm(instance=offer_info)
        return render(request, 'edit_offer.html', {'form': form})

    def post(self, request):
        offer_info = Offer.objects.filter(offer=request.offer).first()
        form = OfferForm(request.POST, instance=offer_info)
        if form.is_valid():
            form.save()
            return redirect('offers_list')

        return render(request, 'edit_offer.html', {'form': form})


class OffersListView(View):

    def get(self, request):
        search_country = request.GET.get('search', '')
        offers = Offer.objects.filter(is_active=True)

        if search_country:
            offers = offers.filter(country__icontains=search_country)

        user = request.user if request.user.is_authenticated else None

        if user:
            ctx = {
                'offers': offers,
                'user': user,
            }
        else:
            ctx = {
                'offers': offers,
            }

        return render(request, 'offers_list.html', ctx)


@method_decorator(login_required, name='dispatch')
class OfferDetailsView(View):

    def get(self, request, name):
        offer = Offer.objects.get(name=name)
        return render(request, 'offer_details.html', {'offer': offer})


class YourOffersCreateView(View):
    def get(self, request):
        return render(request, 'your_offers_create.html')


class YourOffersApplyView(View):
    def get(self, request):
        return render(request, 'your_offers_apply.html')


class MessagesView(View):
    def get(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        messages = Message.objects.filter(receiver=request.user, offer=offer).order_by('time')
        is_offer_owner = offer.owner == request.user
        message_form = MessageForm()

        ctx = {
            'offer': offer,
            'messages': messages,
            'is_offer_owner': is_offer_owner,
            'message_form': message_form
        }
        return render(request, 'messages.html', ctx)

    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        is_offer_owner = offer.owner == request.user
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.sender = request.user
            new_message.receiver = offer.owner
            new_message.offer = offer
            new_message.save()

        return HttpResponseRedirect(request.path)