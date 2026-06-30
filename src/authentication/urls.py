from django.urls import path

from shared.url_names import UrlName

from .views import LoginView, RegisterView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name=UrlName.AUTH_REGISTER),
    path("login/", LoginView.as_view(), name=UrlName.AUTH_LOGIN),
    path("refresh/", TokenRefreshView.as_view(), name=UrlName.AUTH_REFRESH),
]
