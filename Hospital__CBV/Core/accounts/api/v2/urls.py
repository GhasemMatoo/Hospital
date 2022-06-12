from django.urls import path
from .views import RegisterApiViews, CustomAuthToken, CustomDiscardAuthToken
app_name = 'api-v2'
urlpatterns = [
    path('register/', RegisterApiViews.as_view(), name='register'),
    path('login/', CustomAuthToken.as_view(), name='token-login'),
    path('logout/', CustomDiscardAuthToken.as_view(), name='token-logout')

]