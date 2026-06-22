from django.urls import path

from .views import LoginView, TokenRefreshView

urlpatterns = [
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
