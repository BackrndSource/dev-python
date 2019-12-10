from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError
from django.contrib import admin
from django.urls import path, include
from main.models import Setting

try:
    movies = Setting.objects.get(name='slug-movies').value
except (OperationalError, ObjectDoesNotExist) as e:
    movies = 'movies'
    pass
    
try:
    series = Setting.objects.get(name='slug-series').value
except (OperationalError, ObjectDoesNotExist) as e:
    series = 'series'
    pass

try:
    people = Setting.objects.get(name='slug-people').value
except (OperationalError, ObjectDoesNotExist) as e:
    people = 'people'
    pass

urlpatterns = [
    path(movies + '/', include('movies.urls')),
    path(series + '/', include('series.urls')),
    path(people + '/', include('people.urls')),
    path('', include('users.urls')),
    path('', include('main.urls')),
    path('admin/', admin.site.urls),
]
