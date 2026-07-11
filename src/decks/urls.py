from django.urls import path

from shared.url_names import UrlName

from .views import DeckCardsView, DeckDetailView, DeckListView

urlpatterns = [
    path("", DeckListView.as_view(), name=UrlName.DECK_LIST),
    path("<uuid:pk>/", DeckDetailView.as_view(), name=UrlName.DECK_DETAIL),
    path("<uuid:pk>/cards/", DeckCardsView.as_view(), name=UrlName.DECK_CARDS),
]
