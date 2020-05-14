from django.urls import path

from mlplaygrounds.users.views.users import profile

app_name = 'users'
urlpatterns = [
    path('profile/', profile, name='profile')
]

