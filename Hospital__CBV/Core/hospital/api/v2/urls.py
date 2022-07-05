from django.urls import path
from .views import PersonListModelViewSet, PatientStatusListModelViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api-v2'
router = DefaultRouter()
router.register('person', PersonListModelViewSet, basename='person'),
router.register('patient', PatientStatusListModelViewSet, basename='patient')
urlpatterns = router.urls