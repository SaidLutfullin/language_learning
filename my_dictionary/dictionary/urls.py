from django.urls import path
from .views import Dictionary, AddingWord, EditWord, test, cards

urlpatterns = [
    path('dictionary/', Dictionary.as_view(), name='dictionary'),
    path('adding_word', AddingWord.as_view(), name='adding_word'),
    path('test', test, name='test'),
    path('cards', cards, name='cards'),
    path('edit/', EditWord.as_view(), name='edit')
]
