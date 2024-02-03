from django.urls import path
from .views import IndexView, get_forms, get_responses

urlpatterns = [
    #path('', IndexView.as_view(), name='api-index'),
    #path('get-forms/', get_forms, name='get-forms'),
    path('get-responses/<str:form_id>/', get_responses, name='get-responses'),
    path('get-forms/<str:form_id>/', get_forms, name='get-forms'),
]
