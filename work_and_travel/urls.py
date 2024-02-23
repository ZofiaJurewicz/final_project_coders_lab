"""
URL configuration for work_and_travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from work_and_travel_app.views import AddOfferView, YourProfile, AddBaseInfoView, EditBaseInfoView, StartView, \
    OfferDetailsView, EditOfferView, MessagesView, OffersListView, GradeView, MessageBoxView, YourOffers, TopicView, \
    DeleteOfferView, YourGradesView, AnswerToRatingView
from accounts import views as account_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account_view.LoginView.as_view(), name='login_view'),
    path('logout/', account_view.LogoutView.as_view(), name='logout_view'),
    path('register/', account_view.RegistrationView.as_view(), name='register_view'),
    path('', StartView.as_view(), name='start'),
    path('add_offer/', AddOfferView.as_view(), name='add_offer'),
    path('add_base_info/', AddBaseInfoView.as_view(), name='add_base_info'),
    path('edit_base_info/', EditBaseInfoView.as_view(), name='edit_base_info'),
    path('profile/', YourProfile.as_view(), name='your_profile'),
    path('offers_list/', OffersListView.as_view(), name='offers_list'),
    path('offer_details/<int:offer_id>/', OfferDetailsView.as_view(), name='offer_details'),
    path('edit_offer/<int:offer_id>/', EditOfferView.as_view(), name='edit_offer'),
    path('delete_offer_ays/<int:offer_id>', DeleteOfferView.as_view(), name='delete_offer_ays'),
    path('delete_offer/<int:offer_id>/', DeleteOfferView.as_view(), name='delete_offer'),
    path('message_box/', MessageBoxView.as_view(), name='message_box'),
    path('messages/<int:offer_id>/', MessagesView.as_view(), name='messages_view'),
    path('messages/<int:offer_id>/<int:sender_id>/', TopicView.as_view(), name='topic_view'),
    path('rating/<int:offer_id>/<int:sender_id>', GradeView.as_view(), name='grade_view'),
    path('your_offers/', YourOffers.as_view(), name='your_offers'),
    path('your_grades/', YourGradesView.as_view(), name='your_grades'),
    path('rating_answer/<int:grade_id>/', AnswerToRatingView.as_view(), name='answer_view'),
]
