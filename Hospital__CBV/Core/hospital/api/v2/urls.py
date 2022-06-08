from django.urls import path
from .views import PersonListModelViewSet
from rest_framework.routers import DefaultRouter

app_name = 'api-v2'
router = DefaultRouter()
router.register('person', PersonListModelViewSet, basename='person')
urlpatterns = router.urls