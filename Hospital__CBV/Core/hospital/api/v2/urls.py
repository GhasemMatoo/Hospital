from django.urls import path
from .views import PersonList, PersonDetail

app_name = 'api-v2'

urlpatterns = [
    path('person/', PersonList.as_view(), name='person'),
    path('person/<int:national_code>', PersonDetail.as_view(), name='person_detail'),
]