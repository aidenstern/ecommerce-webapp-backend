from django.urls import path

from .views import (
    AccountRegistration,
    AccountLogin,
    AccountLogout,
    SocialLogin,
)


urlpatterns = [
    # token login/logout api view
    path('user/login/', AccountLogin.as_view()),
    path('user/register/', AccountRegistration.as_view()),
    path('user/logout/', AccountLogout.as_view()),

    # social login/register api view
    path('user/social/login/', SocialLogin.as_view()),
]
