from django.urls import path
from .views import (RegisterApiViews, CustomAuthToken,
                    CustomDiscardAuthToken, CustomTokenObtainPairView, ChangePasswordApiViews,
                    ProfileApiViews, ActivationApiViews, ResendActivationApiViews)
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

app_name = 'api-v2'


urlpatterns = [
    path('register/', RegisterApiViews.as_view(), name='register'),
    path('change-password/', ChangePasswordApiViews.as_view(), name='change-password'),
    path('activation/conform/<str:token>', ActivationApiViews.as_view(), name='activation'),
    path('activation/resend/', ResendActivationApiViews.as_view(), name='resend-activation'),
    # AuthToken
    path('login/', CustomAuthToken.as_view(), name='token-login'),
    path('logout/', CustomDiscardAuthToken.as_view(), name='token-logout'),
    # JWT
    path('jwt/token/create', CustomTokenObtainPairView.as_view(), name='create-token'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # Profile
    path('profile/user/', ProfileApiViews.as_view(), name='profile'),
]