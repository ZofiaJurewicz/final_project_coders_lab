from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, Prefetch, Avg, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from work_and_travel_app.forms import OfferForm, AddBaseInfoForm, MessageForm, GradeForm, AnswerForm
from work_and_travel_app.models import BaseInformation, Offer, Message, Category, Grade, Answer


class StartView(View):

    def get(self, request):
        search_country = request.GET.get('search', '')
        offers = Offer.objects.filter(is_active=True)

        if search_country:
            return HttpResponseRedirect(f'/offers_list/?search={search_country}')

        return render(request, 'start.html')


class YourProfile(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        base_info = BaseInformation.objects.filter(user=user).first()

        grades_received = Grade.objects.filter(
            message__offer__owner=request.user
        ).aggregate(
            avg_grade=Coalesce(Avg('grade'), 0, output_field=FloatField())
        )['avg_grade']

        answers_received = Answer.objects.filter(
            answer__message__offer__owner=request.user
        ).aggregate(
            avg_grade_answer=Coalesce(Avg('grade_answer'), 0, output_field=FloatField())
        )['avg_grade_answer']

        avg_grade = (grades_received + answers_received) / 2 if (grades_received + answers_received) > 0 else 0

        return render(request, 'your_profile.html', {'user': user, 'base_info': base_info, 'avg_grade': avg_grade})


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

            categories_ids_list = request.POST.getlist('category')
            for category_id in categories_ids_list:
                category = Category.objects.get(id=category_id)
                offer.category.add(category)

            offer.save()
            return redirect('offers_list')

        return render(request, 'add_offer.html', {'form': form, 'categories': categories})


class EditOfferView(LoginRequiredMixin, View):

    def get(self, request, offer_id):
        try:
            offer = Offer.objects.get(id=offer_id, owner=request.user)
        except Offer.DoesNotExist:
            return redirect('offers_list')
        offer_info = Offer.objects.get(id=offer_id)
        form = OfferForm(instance=offer_info)
        return render(request, 'edit_offer.html', {'form': form, 'offer_id': offer_id, 'offer': offer})

    def post(self, request, offer_id):
        try:
            offer = Offer.objects.get(id=offer_id, owner=request.user)
        except Offer.DoesNotExist:
            return redirect('offers_list')
        offer_info = get_object_or_404(Offer, id=offer_id)
        form = OfferForm(request.POST, instance=offer_info)
        if form.is_valid():
            form.save()
            return redirect('offers_list')

        return render(request, 'edit_offer.html', {'form': form, 'offer_id': offer_id, 'offer': offer})


class DeleteOfferView(LoginRequiredMixin, View):
    def get(self, request, offer_id):
        try:
            offer = Offer.objects.get(id=offer_id, owner=request.user)
        except Offer.DoesNotExist:
            return redirect('offers_list')
        offer = get_object_or_404(Offer, id=offer_id)
        return render(request, 'are_you_sure_delete.html')

    def post(self, request, offer_id):
        try:
            offer = Offer.objects.get(id=offer_id, owner=request.user)
        except Offer.DoesNotExist:
            return redirect('offers_list')

        offer_info = get_object_or_404(Offer, id=offer_id)
        offer_info.delete()
        return redirect('offers_list')


class OffersListView(View):

    def get(self, request):
        search_country = request.GET.get('search', '')
        offers = Offer.objects.filter(is_active=True)
        if search_country:
            offers = offers.filter(country__icontains=search_country)

        categories = Category.objects.all()
        paginator = Paginator(offers, 2)
        page = request.GET.get('page', 1)
        print(page)
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


class YourOffers(LoginRequiredMixin, View):
    def get(self, request):
        offers = Offer.objects.filter(owner=request.user).order_by('until_when')
        return render(request, 'your_offers.html', {'offers': offers})


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
        )
        conversations = {}
        for offer in offers_involved:
            conversations[offer] = Message.objects.filter(
                Q(offer=offer) &
                (Q(receiver=request.user) | Q(sender=request.user))
            ).order_by('time')

        return render(request, 'messages_box.html', {'conversations': conversations})


class MessagesView(LoginRequiredMixin, View):
    def get(self, request, offer_id):
        offer = get_object_or_404(Offer, pk=offer_id)
        q1 = Q(offer_id=offer_id)
        q2 = Q(sender=request.user)
        q3 = Q(receiver=request.user)

        messages = Message.objects.filter(q1, q2 | q3).distinct().order_by('-time').select_related('sender', 'receiver')

        conversations = {}
        for message in messages:
            partner = message.receiver if message.sender == request.user else message.sender
            key = (request.user, partner) if request.user.id < partner.id else (partner, request.user)

            if key not in conversations:
                conversations[key] = {
                    'last_message': message,
                    'partner': partner,
                    'messages': []
                }

            conversations[key]['messages'].append(message)

        sorted_conversations = sorted(conversations.values(), key=lambda x: x['last_message'].time, reverse=True)

        return render(request, 'messages_view.html', {'conversations': sorted_conversations, 'offer': offer})


class TopicView(LoginRequiredMixin, View):

    def get(self, request, offer_id, sender_id):
        offer = get_object_or_404(Offer, pk=offer_id)
        messages = Message.objects.filter(offer_id=offer_id)
        messages = messages.filter(sender_id=sender_id) | messages.filter(receiver_id=sender_id)
        messages = messages.order_by('time')
        message_form = MessageForm
        return render(request, 'topic_view.html',
                      {'messages': messages, 'message_form': message_form, 'offer': offer, 'sender_id': sender_id})

    def get_receiver(self, offer_id, sender_id):
        offer = Offer.objects.get(pk=offer_id)
        if offer.owner == self.request.user:
            return sender_id
        else:
            return offer.owner_id

    def post(self, request, offer_id, sender_id):
        messages = Message.objects.filter(offer_id=offer_id)
        messages = messages.filter(sender_id=sender_id) | messages.filter(receiver_id=sender_id)
        messages = messages.order_by('time')
        message_form = MessageForm(request.POST)

        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.offer_id = offer_id
            new_message.sender = request.user
            new_message.receiver_id = self.get_receiver(offer_id, sender_id)
            new_message.save()
            return redirect('topic_view', offer_id=offer_id, sender_id=sender_id)

        return render(request, 'topic_view.html', {'messages': messages, 'message_form': message_form})


class GradeView(LoginRequiredMixin, View):
    def get(self, request, offer_id, sender_id):
        offer = get_object_or_404(Offer, pk=offer_id)
        first_message_sender = get_object_or_404(User, pk=sender_id)
        if (request.user == offer.owner):
            messages = Message.objects.filter(offer_id=offer_id, sender_id=sender_id).order_by('-time')
            if messages:
                message = messages.first()
            else:
                message = None

            try:
                grade = Grade.objects.get(message=message)
            except Grade.DoesNotExist:
                grade = None

            answer = Answer.objects.filter(answer=grade).first()
            form = GradeForm(instance=grade)

            ctx = {
                'form': form,
                'message': message,
                'offer': offer,
                'first_message_sender': first_message_sender,
                'answer': answer,
            }

            return render(request, 'grade.html', ctx)
        else:
            return redirect('messages_view', offer_id=offer_id)

    def post(self, request, offer_id, sender_id):
        offer = get_object_or_404(Offer, pk=offer_id)
        first_message_sender = get_object_or_404(User, pk=sender_id)

        messages = Message.objects.filter(offer_id=offer_id, sender_id=sender_id).order_by(
            '-time')
        if messages:
            message = messages.first()
        else:
            message = None

        try:
            grade = Grade.objects.get(message=message)
        except Grade.DoesNotExist:
            grade = Grade(user=message.sender, message=message)

        answer = Answer.objects.filter(answer=grade).first()
        form = GradeForm(request.POST, instance=grade)

        if form.is_valid():
            form.save()
            return redirect('grade_view', offer_id=offer_id, sender_id=sender_id)

        ctx = {
            'form': form,
            'message': message,
            'offer': offer,
            'first_message_sender': first_message_sender,
            'answer': answer
        }

        return render(request, 'grade.html', ctx)


class YourGradesView(LoginRequiredMixin, View):
    def get(self, request):
        grades = Grade.objects.filter(message__sender=request.user) \
            .select_related('message') \
            .prefetch_related(Prefetch('message__offer', queryset=Offer.objects.all())) \
            .order_by('-message__offer__name')

        ctx = {
            'grades_list': [{
                'id': grade.id,
                'offer_names': grade.message.offer.name,
                'owner_names': grade.message.offer.owner.username,
                'grade_value': grade.grade,
            }
                for grade in grades
            ]}

        return render(request, 'your_grades.html', ctx)


class AnswerToRatingView(LoginRequiredMixin, View):
    def get(self, request, grade_id):
        grade = get_object_or_404(Grade, pk=grade_id)
        try:
            answer = Answer.objects.get(answer=grade)
            if answer.answer.user != request.user:
                return redirect('your_grades')
            form = AnswerForm(instance=answer)
        except Answer.DoesNotExist:
            form = AnswerForm()
        return render(request, 'answer.html', {'grade': grade, 'form': form})

    def post(self, request, grade_id):
        grade = get_object_or_404(Grade, pk=grade_id)
        try:
            answer = Answer.objects.get(answer=grade)
            if answer.answer.user != request.user:
                return redirect('your_grades')
            form = AnswerForm(request.POST, instance=answer)
        except Answer.DoesNotExist:
            form = AnswerForm(request.POST)

        if form.is_valid():
            answer = form.save(commit=False)
            answer.answer = grade
            answer.save()
            return redirect('answer_view', grade_id=grade.id)
        return render(request, 'answer.html', {'grade': grade, 'form': form})
