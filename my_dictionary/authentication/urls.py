from django.urls import path
from .views import LoginUser, RegisterUser, logout_user, MyProfile, MyProfileEdit, ChangePassword, ChangePasswordDone

urlpatterns = [
    path('login', LoginUser.as_view(), name='login'),
    path('register', RegisterUser.as_view(), name='register'),
    path('logout', logout_user, name='logout'),

    path('change_password', ChangePassword.as_view(), name='password_change'),
    path('change_password/done/', ChangePasswordDone.as_view(), name='password_change_done'),
    
    path('my_pfofile', MyProfile.as_view(), name='my_profile'),
    path('my_pfofile/edit', MyProfileEdit.as_view(), name='my_profile_edit'),
]
