# apii/urls.pyform_detail

from django.urls import path
from .views import  get_all_forms ,get_form,edit_form


 

urlpatterns = [
    #path('forms/<int:form_id>/', get_forms, name='get_forms'),
    path('get_all_forms/', get_all_forms, name='get_all_forms'),
    #path('update_form/<str:form_id>/', update_form, name='update_form'),
    #path('forms/<str:form_id>/', form_detail, name='form_detail'),
    path('get_form/<str:form_id>/', get_form, name='get_form'),
    path('edit_form/<str:form_id>/', edit_form, name='edit_form'),
]
