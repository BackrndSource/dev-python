from django.urls import path
from .views import SeriesHomeView, SeriesDetailView, SeriesSearchView, SeriesPopularView, SeriesUpcomingView, SeriesTopRatedView
from main.models import Setting

app_name = 'series'
search = Setting.objects.get(name='slug-series-search').value
popular = Setting.objects.get(name='slug-series-popular').value
upcoming = Setting.objects.get(name='slug-series-upcoming').value
top_rated = Setting.objects.get(name='slug-series-toprated').value

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