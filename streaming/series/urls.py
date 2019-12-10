from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import OperationalError
from django.urls import path
from .views import SeriesHomeView, SeriesDetailView, SeriesSearchView, SeriesPopularView, SeriesUpcomingView, SeriesTopRatedView
from main.models import Setting

try:
    search = Setting.objects.get(name='slug-series-search').value
except (OperationalError, ObjectDoesNotExist) as e:
    search = 'search'
    pass
    
try:
    popular = Setting.objects.get(name='slug-series-popular').value
except (OperationalError, ObjectDoesNotExist) as e:
    popular = 'popular'
    pass

try:
    upcoming = Setting.objects.get(name='slug-series-upcoming').value
except (OperationalError, ObjectDoesNotExist) as e:
    upcoming = 'upcoming'
    pass

try:
    top_rated = Setting.objects.get(name='slug-series-toprated').value
except (OperationalError, ObjectDoesNotExist) as e:
    top_rated = 'top_rated'
    pass

app_name = 'series'
urlpatterns = [
    path('', SeriesHomeView.as_view(), name='home'),
    path('<int:id>/', SeriesDetailView.as_view(), name='detail'),
    path('<int:id>/<str:slug>/', SeriesDetailView.as_view(), name='detail'),
    path(search + '/', SeriesSearchView.as_view(), name='search'),
    path(popular + '/', SeriesPopularView.as_view(), name='popular'),
    path(popular + '/<int:page>/', SeriesPopularView.as_view(), name='popular'),
    path(upcoming + '/', SeriesUpcomingView.as_view(), name='upcoming'),
    path(upcoming + '/<int:page>/', SeriesUpcomingView.as_view(), name='upcoming'),
    path(top_rated + '/', SeriesTopRatedView.as_view(), name='top_rated'),
    path(top_rated + '/<int:page>/', SeriesTopRatedView.as_view(), name='top_rated'),
]