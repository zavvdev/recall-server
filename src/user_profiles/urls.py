from django.urls import path

from shared.url_names import UrlName

from .views import UserProfileView

urlpatterns = [
    path("", UserProfileView.as_view(), name=UrlName.USER_PROFILE),
]
