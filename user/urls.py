from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterUser,
    EmailTokenObtainPairWithUserDataView,
    UsernameTokenObtainPairWithUserDataView,
)

urlpatterns = [
    url(r'^v1/accounts/token/$',
        EmailTokenObtainPairWithUserDataView.as_view(),
        name='token_obtain_pair'),
    url(r'^v1/accounts/token-by-username/$',
        UsernameTokenObtainPairWithUserDataView.as_view(),
        name='username_token_obtain_pair'),
    url(r'^v1/accounts/token/refresh/$',
        TokenRefreshView.as_view(),
        name='token_refresh'),
    url(r'^v1/accounts/register/$',
        RegisterUser.as_view(),
        name='register_user'),  
]