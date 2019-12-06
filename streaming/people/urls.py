from django.urls import path
from .views import PeoplePopularView, PeopleDetailView, PeopleSearchView
from main.models import Setting

app_name = 'people'
search = 'search'
#search = Setting.objects.get(name='slug-people-search').value
popular = 'popular'
#popular = Setting.objects.get(name='slug-people-popular').value

urlpatterns = [
    path('', PeoplePopularView.as_view(), name='home'),
    path('<int:id>/', PeopleDetailView.as_view(), name='detail'),
    path('<int:id>/<str:slug>/', PeopleDetailView.as_view(), name='detail'),
    path(search + '/', PeopleSearchView.as_view(), name='search'),
    path(popular + '/', PeoplePopularView.as_view(), name='popular'),
    path(popular + '/<int:page>/', PeoplePopularView.as_view(), name='popular'),
]