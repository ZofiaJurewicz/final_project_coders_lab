from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView

from work_and_travel_app.forms import OfferForm, AddBaseInfoForm, MessageForm, GradeForm
from work_and_travel_app.models import BaseInformation, Offer, Message, Category, Grade


class StartView(View):

    def get(self, request):
        search_country = request.GET.get('search', '')
        offers = Offer.objects.filter(is_active=True)

        if search_country:
            offers = offers.filter(country__icontains=search_country)
            return render(request, 'offers_list.html', {'offers': offers})

        return render(request, 'start.html')


class YourProfile(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        base_info = BaseInformation.objects.all()
        return render(request, 'your_profile.html', {'user': user, 'base_info': base_info})


class AddBaseInfoView(LoginRequiredMixin, View):

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


class EditBaseInfoView(LoginRequiredMixin, View):

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


class AddOfferView(LoginRequiredMixin, View):
    def get(self, request):
        form = OfferForm()
        categories = Category.objects.all()
        return render(request, 'add_offer.html', {'form': form, 'categories': categories})

    def post(self, request):
        form = OfferForm(request.POST)
        categories = Category.objects.all()
        if form.is_valid():
            offer = form.save(commit=False)
            offer.owner = request.user
            offer.save()
            return redirect('offers_list')

        return render(request, 'add_offer.html', {'form': form, 'categories': categories})


class EditOfferView(LoginRequiredMixin, View):

    def get(self, request, offer_id):
        offer_info = Offer.objects.get(id=offer_id)
        form = OfferForm(instance=offer_info)
        return render(request, 'edit_offer.html', {'form': form, 'offer_id': offer_id})

    def post(self, request, offer_id):
        offer_info = get_object_or_404(Offer, id=offer_id)
        form = OfferForm(request.POST, instance=offer_info)
        if form.is_valid():
            form.save()
            return redirect('offers_list')

        return render(request, 'edit_offer.html', {'form': form, 'offer_id': offer_id})


class OffersListView(View):

    def get(self, request):
        search_country = request.GET.get('search', '')
        offers = Offer.objects.filter(is_active=True)
        categories = Category.objects.all()
        paginator = Paginator(offers, 2)
        page = request.GET.get('page')
        offers_list = paginator.get_page(page)

        if search_country:
            offers = offers.filter(country__icontains=search_country)

        user = request.user if request.user.is_authenticated else None

        if user:
            ctx = {
                'offers': offers,
                'user': user,
                'offers_list': offers_list,
                'categories': categories,
            }
        else:
            ctx = {
                'offers': offers,
                'offers_list': offers_list,
                'categories': categories,
            }

        return render(request, 'offers_list.html', ctx)


class OfferDetailsView(View):

    def get(self, request, offer_id):
        offer = Offer.objects.get(id=offer_id)
        categories = Category.objects.all()
        return render(request, 'offer_details.html', {'offer': offer, 'categories': categories})


class MessageBoxView(LoginRequiredMixin, View):
    def get(self, request):

        offers_involved = Offer.objects.filter(
            Q(message__sender=request.user) |
            Q(message__receiver=request.user)
        ).distinct()

        conversations = {}
        for offer in offers_involved:
            conversations[offer] = Message.objects.filter(
                Q(offer=offer) &
                (Q(receiver=request.user) | Q(sender=request.user))
            ).order_by('time')

        return render(request, 'messages_box.html', {'conversations': conversations})


class MessagesView(LoginRequiredMixin, View):
    def get(self, request, offer_id, sender_username):
        offer = Offer.objects.get(id=offer_id)
        sender_user = get_object_or_404(User, username=sender_username)

        message_ids_for_sender = Message.objects.filter(
            offer=offer,
            sender=sender_user
        ).values_list('id', flat=True)

        message_ids_for_receiver = Message.objects.filter(
            offer=offer,
            receiver=sender_user
        ).values_list('id', flat=True)

        all_message_ids = set(list(message_ids_for_sender) + list(message_ids_for_receiver))

        messages = Message.objects.filter(id__in=all_message_ids).order_by('time')

        form = MessageForm()
        ctx = {
            'offer': offer,
            'form': form,
            'messages': messages,
            'sender_user': sender_user,
        }
        return render(request, 'messages_view.html', ctx)

    def post(self, request, offer_id, sender_username=None):
        offer = Offer.objects.get(id=offer_id)
        form = MessageForm(request.POST)
        sender_user = get_object_or_404(User, username=sender_username) if sender_username else request.user

        if form.is_valid():
            message = form.save(commit=False)
            message.offer = offer
            message.sender = request.user
            message.receiver = offer.owner
            message.save()
            return redirect('message_view', offer_id=offer_id, sender_username=sender_username)
        else:
            messages = Message.objects.filter(
                offer=offer,
                sender=sender_user,
                receiver=offer.owner
            ) | Message.objects.filter(
                offer=offer,
                receiver=sender_user,
                sender=offer.owner
            ).distinct().order_by('time')
            return render(request, 'messages_view.html', {
                'offer': offer,
                'messages': messages,
                'form': form,
                'sender_user': sender_user
            })


class GradeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'grade.html')

    def post(self, request):
        return render(request, 'grade.html')


class YourOffers(LoginRequiredMixin, View):
    def get(self, request):
        offers = Offer.objects.filter(owner=request.user).order_by('until_when')
        return render(request, 'your_offers.html', {'offers': offers})
