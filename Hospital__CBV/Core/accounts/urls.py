from django.urls import path, include

app_name = "accounts"

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('api/v2/', include('accounts.api.v2.urls')),
]