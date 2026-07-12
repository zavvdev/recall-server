from django.urls import path

from shared.url_names import UrlName

from .views import CardListView

urlpatterns = [
    path("", CardListView.as_view(), name=UrlName.CARD_LIST),
]
