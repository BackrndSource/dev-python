from django.urls import path
from .views import MoviesHomeView, MoviesDetailView, MoviesSearchView, MoviesPopularView, MoviesUpcomingView, MoviesTopRatedView
from main.models import Setting

app_name = 'movies'
search = Setting.objects.get(name='slug-movies-search').value
popular = Setting.objects.get(name='slug-movies-popular').value
upcoming = Setting.objects.get(name='slug-movies-upcoming').value
top_rated = Setting.objects.get(name='slug-movies-toprated').value

urlpatterns = [
    path('', MoviesHomeView.as_view(), name='home'),
    path('<int:id>/', MoviesDetailView.as_view(), name='detail'),
    path('<int:id>/<str:slug>/', MoviesDetailView.as_view(), name='detail'),
    path(search + '/', MoviesSearchView.as_view(), name='search'),
    path(popular + '/', MoviesPopularView.as_view(), name='popular'),
    path(popular + '/<int:page>/', MoviesPopularView.as_view(), name='popular'),
    path(upcoming + '/', MoviesUpcomingView.as_view(), name='upcoming'),
    path(upcoming + '/<int:page>/', MoviesUpcomingView.as_view(), name='upcoming'),
    path(top_rated + '/', MoviesTopRatedView.as_view(), name='top_rated'),
    path(top_rated + '/<int:page>/', MoviesTopRatedView.as_view(), name='top_rated'),
]