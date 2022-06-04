from django.urls import path, include
from .views import PersonViews, PersonDetailViews, PersonDeleteViews, PersonFormViews, PersonHomeViews

app_name = 'hospital'

urlpatterns = [
    path('', PersonHomeViews.as_view(), name="person_home"),
    path('person/', PersonViews.as_view(), name='person'),
    path('person/detail/<slug:national_code>', PersonDetailViews.as_view(), name="person_detail"),
    path('person/delete/<slug:national_code>', PersonDeleteViews.as_view(), name="person_delete"),
    path('person/forms/', PersonFormViews.as_view(), name="person_forms"),
    path('api/v1/', include('hospital.api.v1.urls'))

]