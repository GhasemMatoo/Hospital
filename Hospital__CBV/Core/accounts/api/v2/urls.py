from django.urls import path
from .views import RegisterApiViews, CustomAuthToken, CustomDiscardAuthToken, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'api-v2'


urlpatterns = [
    path('register/', RegisterApiViews.as_view(), name='register'),
    # AuthToken
    path('login/', CustomAuthToken.as_view(), name='token-login'),
    path('logout/', CustomDiscardAuthToken.as_view(), name='token-logout'),
    # JWT
    path('jwt/token/create', CustomTokenObtainPairView.as_view(), name='create-token'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]