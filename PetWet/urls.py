"""PetWet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include
from Administrator import views
from CommonHome import cviews
from Login_Register import lviews
from Owner import oviews
from PetShop import pviews
from Veterinary import vviews
from Walkers import wviews

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static


urlpatterns = [
   

    path('',cviews.index),

    path('admin_header_footer/',views.admin_header_footer),
    path('admin_home/',views.admin_home),
    path('pet_owners/',views.pet_owners),
    path('owner_remove/',views.owner_remove),
    path('walkers_request/',views.walkers_request),
    path('walker_action/',views.walker_action),
    path('walkers_list/',views.walkers_list),
    path('veterinary_request/',views.veterinary_request),
    path('veterinary_action/',views.veterinary_action),
    path('veterinary_list/',views.veterinary_list),
    path('shop_request/',views.shop_request),
    path('shop_action/',views.shop_action),
    path('shop_list/',views.shop_list),
    path('view_complaints/',views.view_complaints),
    path('add_category/',views.add_category),
    path('cat_action/',views.cat_action),


    path('login/',lviews.login),
    path('owner_register/',lviews.owner_register),
    path('walker_register/',lviews.walker_register),
    path('clinic_register/',lviews.clinic_register),
    path('shop_register/',lviews.shop_register),


    path('owner_header_footer/',oviews.owner_header_footer),
path('owner_home/',oviews.owner_home),
path('send_complaints/',oviews.send_complaints),
path('view_walkers/',oviews.view_walkers),
path('owner_view_walkers/',oviews.owner_view_walkers),
path('walker_request_form/',oviews.walker_request_form),
path('walker_request_status/',oviews.walker_request_status),
path('request_action/',oviews.request_action),
path('view_pet_centre/',oviews.view_pet_centre),
path('view_pet_centre_profile/',oviews.view_pet_centre_profile),
path('view_petcentre_product/',oviews.view_petcentre_product),
path('send_lookafter_request/',oviews.send_lookafter_request),
path('owner_lookafter_request/',oviews.owner_lookafter_request),
path('owner_show_pets/',oviews.owner_show_pets),
path('owner_view_pet/',oviews.owner_view_pet),
path('send_pet_adoption_request/',oviews.send_pet_adoption_request),
path('owner_adoption_status/',oviews.owner_adoption_status),
path('del_adoption_request/',oviews.del_adoption_request),
path('owner_view_veterinary/',oviews.owner_view_veterinary),
path('view_vet_dr_list/',oviews.view_vet_dr_list),
path('send_dr_appointment/',oviews.send_dr_appointment),
path('owner_view_booking/',oviews.owner_view_booking),
path('del_booking_request/',oviews.del_booking_request),


 path('vet_header_footer/',vviews.vet_header_footer),
path('vet_home/',vviews.vet_home),
path('vet_profile/',vviews.vet_profile),
path('add_doctor/',vviews.add_doctor),
path('view_doctors/',vviews.view_doctors),
path('view_doctor_detail/',vviews.view_doctor_detail),
path('del_dr_detail/',vviews.del_dr_detail),
path('view_bk_requests/',vviews.view_bk_requests),
path('booking_action/',vviews.booking_action),




path('pet_header_footer/',pviews.pet_header_footer),
path('pet_home/',pviews.pet_home),
path('shop_profile/',pviews.shop_profile),
path('add_product/',pviews.add_product),
path('view_product/',pviews.view_product),
path('shop_view_item/',pviews.shop_view_item),
path('pet_request_action/',pviews.pet_request_action),
path('add_pet/',pviews.add_pet),
path('pet_lookafter_request/',pviews.pet_lookafter_request),
path('pets_list/',pviews.pets_list),
path('del_product/',pviews.del_product),
path('view_pet_detail/',pviews.view_pet_detail),
path('del_pet_detail/',pviews.del_pet_detail),
path('pet_adoption_request/',pviews.pet_adoption_request),
path('pet_adoption_request_action/',pviews.pet_adoption_request_action),



path('walkers_header_footer/',wviews.walkers_header_footer),
path('walkers_home/',wviews.walkers_home),
path('walkers_profile/',wviews.walkers_profile),
path('new_request/',wviews.new_request),
path('new_request_action/',wviews.new_request_action),
path('request_status/',wviews.request_status),
path('add_amount/',wviews.add_amount),
path('add_message/',wviews.add_message),
path('request_approve_action/',wviews.request_approve_action),


]
# ]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
