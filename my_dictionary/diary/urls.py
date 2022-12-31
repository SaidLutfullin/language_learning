from django.urls import path
from .views import NewDay, MyDiary, ShowDay, EditDay, DeleteDay

urlpatterns = [
    path('new_day', NewDay.as_view(), name='new_day'),
    path('my_diary', MyDiary.as_view(), name='my_diary'),
    path('my_diary/<int:day>', ShowDay.as_view(), name='concrete_day'),
    path('my_diary/<int:day>/edit', EditDay.as_view(), name='edit_day'),
    path('my_diary/<int:day>/delete', DeleteDay.as_view(), name='delete_day')
]
