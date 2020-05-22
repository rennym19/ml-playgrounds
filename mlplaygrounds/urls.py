from django.contrib import admin
from django.urls import path, include

from mlplaygrounds.users import urls as users_urls
from mlplaygrounds.datasets import urls as datasets_urls
from mlplaygrounds.frontend import urls as frontend_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(users_urls)),
    path('data/', include(datasets_urls)),
    path('', include(frontend_urls))
]
