from django.urls import path

from shared.url_names import UrlName

from .views import CardDetailView, CardListView

urlpatterns = [
    path("", CardListView.as_view(), name=UrlName.CARD_LIST),
    path("<uuid:pk>/", CardDetailView.as_view(), name=UrlName.CARD_DETAIL),
]
