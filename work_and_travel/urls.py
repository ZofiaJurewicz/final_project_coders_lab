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
    OffersListLoginView, OfferDetailsView, EditOfferView, YourOffersCreateView, YourOffersApplyView, MessagesView, \
    OffersListView
from accounts import views as account_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account_view.LoginView.as_view(), name='login_view'),
    path('logout/', account_view.LogoutView.as_view(), name='logout_view'),
    path('register/', account_view.RegistrationView.as_view(), name='register_view'),
    path('start/', StartView.as_view(), name='start'),
    path('add_offer/', AddOfferView.as_view(), name='add_offer'),
    path('add_base_info/', AddBaseInfoView.as_view(), name='add_base_info'),
    path('edit_base_info/', EditBaseInfoView.as_view(), name='edit_base_info'),
    path('profile/', YourProfile.as_view(), name='your_profile'),
    path('offers_list_log/', OffersListLoginView.as_view(), name='offers_list_login'),
    path('offers_list/', OffersListView.as_view(), name='offers_list'),
    path('offer_details_log/<str:name>/', OfferDetailsView.as_view(), name='offer_details_log'),
    path('offer_details/<str:name>/', OfferDetailsView.as_view(), name='offer_details'),
    path('edit_offer/', EditOfferView.as_view(), name='edit_offer'),
    path('your_offers_create', YourOffersCreateView.as_view(), name='your_offers_create'),
    path('your_offers_apply', YourOffersApplyView.as_view(), name='your_offers_apply'),
    path('messages', MessagesView.as_view(), name='message_view')
]

