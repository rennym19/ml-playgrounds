from django.urls import path

from mlplaygrounds.users.views.users import profile
from mlplaygrounds.users.views.auth import Login, Register

from knox import views as knox_views

app_name = 'users'
urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logout-all/', knox_views.LogoutAllView.as_view(), name='logout-all'),
    path('register/', Register.as_view(), name='register'),
    path('profile/', profile, name='profile')
]

