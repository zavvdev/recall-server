from django.urls import path

from shared.url_names import UrlName

from .views import CardView

urlpatterns = [
    path("", CardView.as_view(), name=UrlName.CARD),
]
