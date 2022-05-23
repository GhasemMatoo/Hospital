from django.urls import path
from hospital.views import *

app_name = "hospital"

urlpatterns = [
    path("", home_views, name='home'),
    path('person/', person_views, name='person'),
    path('person/form', person_form_views, name='person_form'),
    path('person/delete/<str:national_code>', person_views, name='delete_person'),
    path('person/update/<str:national_code>', person_update_views, name='person_update'),
    path('person/upload/excel', person_upload_excel_views, name='upload_excel'),
]