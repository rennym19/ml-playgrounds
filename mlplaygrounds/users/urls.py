from django.urls import path

from mlplaygrounds.users.views import hello

appname = 'users'
urlpatterns = [
    path('', hello, name='hello')
]

