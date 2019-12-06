"""coolcats URL Configuration

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
from django.contrib import admin
from django.urls import path
from api.views import login, get_users
from django.conf.urls import url
from api import views as api_views
from form_response_service import views as form_response_service_views
from form_admin_service import views as form_admin_service_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', login, name="login"),
    path('api/get_all_users/', api_views.get_users, name='get_users'),
    path('api/get_user_by_username/', api_views.get_user_by_username, name='get_user_by_username'),

    path('form_admin_service/add_form/', form_admin_service_views.add_form, name='service_add_form'),
    path('form_admin_service/get_form/', form_admin_service_views.get_form_by_id, name='service_get_form'),
    path('form_admin_service/get_all_forms/', form_admin_service_views.get_all_forms, name='service_get_all_forms'),
    path('form_admin_service/delete_form/', form_admin_service_views.delete_form, name='service_delete_form'),

    path('form_response_service/get_form_response/', form_response_service_views.get_form_response, name='service_get_form_response'),
    path('form_response_service/delete_form_response/', form_response_service_views.delete_form_response, name='service_delete_form_response'),
    path('form_response_service/get_all_form_responses/', form_response_service_views.get_all_form_responses, name='service_get_all_form_responses'),
    path('form_response_service/submit_form_response/', form_response_service_views.submit_form_response, name='service_submit_form_response'),
    path('form_response_service/get_answer/', form_response_service_views.get_answer, name='service_get_answer'),

    path('api/add_form/', api_views.add_form, name='add_form'),
    path('api/submit_form_response/', api_views.submit_form_response, name='submit_form_response'),
    path('api/get_form_by_id/', api_views.get_form_by_id, name='get_form_by_id'),
    path('api/get_all_forms/', api_views.get_all_forms, name='get_all_forms'),
    path('api/delete_form/', api_views.delete_form, name='delete_form'),


    path('api/get_form_response/', api_views.get_form_response, name='get_form_response'),
    path('api/get_all_form_responses/', api_views.get_all_form_responses, name='get_all_form_responses'),
    path('api/delete_form_response/', api_views.delete_form_response, name='delete_form_response'),
]
