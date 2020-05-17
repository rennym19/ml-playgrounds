from django.urls import path

from mlplaygrounds.users.views.users import profile
from mlplaygrounds.users.views.auth import Login, Logout, Register

app_name = 'users'
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('register/', Register.as_view(), name='register'),
    path('profile/', profile, name='profile')
]

