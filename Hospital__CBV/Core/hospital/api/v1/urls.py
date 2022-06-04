from django.urls import path
from .views import person_views, person_detail_views

app_name = 'api-v1'

urlpatterns = [
    path('person/', person_views, name='person'),
    path('person/<int:national_code>', person_detail_views, name='person_detail'),
]