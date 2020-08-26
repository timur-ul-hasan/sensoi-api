from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterUser,
    EmailTokenObtainPairWithUserDataView,
    UsernameTokenObtainPairWithUserDataView,
)

urlpatterns = [
    url(r'^accounts/token/$',
        EmailTokenObtainPairWithUserDataView.as_view(),
        name='token_obtain_pair'),
    url(r'^accounts/token-by-username/$',
        UsernameTokenObtainPairWithUserDataView.as_view(),
        name='username_token_obtain_pair'),
    url(r'^accounts/token/refresh/$',
        TokenRefreshView.as_view(),
        name='token_refresh'),
    url(r'^accounts/register/$',
        RegisterUser.as_view(),
        name='register_user'),  
]