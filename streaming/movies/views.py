from django.shortcuts import render, redirect
from django.urls import reverse
from tmdbv3api import Movie, Discover, Genre
from main.views import DiscoverView, TmdbDetailView, SearchView
from sites.models import Site
from links.models import Link
from django.db.models import Q
import time


class MoviesListMixin():

    def get(self, request, *args, **kwargs):
        self.genre_list = Genre().movie_list()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.genre_list = Genre().movie_list()
        return super().post(request, *args, **kwargs)


class MoviesDetailMixin():
    type = 1

    def prepare_site_list(self):
        self.site_list = Site.objects.filter(Q(type=0) | Q(type=self.type))
        super().prepare_site_list()

    def prepare_link_list(self):
        self.link_list = Link.objects.filter(Q(post__tmdb_id=self.id) | Q(post__type=self.type))
        super().prepare_site_list()


class MoviesHomeView(MoviesListMixin, DiscoverView):
    title = 'Movies Home'
    view_path = 'movies:home'
    paginate = False
    template_name = 'main/home.html'
    discover_method = 'discover_movies'

    def prepare_context_list(self):
        self.discover_params = {'primary_release_date.gte':time.strftime('%Y-%m-%d'), 'sort_by':'popularity.desc'}
        self.set_discover_params()
        self.get_result_list()
        self.context['data']['upcoming_list'] = self.result_list[:6]

        self.discover_params = {'primary_release_date.lte':time.strftime('%Y-%m-%d'), 'sort_by':'popularity.desc'}
        self.set_discover_params()
        self.get_result_list()
        self.context['data']['popular_list'] = self.result_list[:12]

        self.discover_params = {'primary_release_date.lte':time.strftime('%Y-%m-%d'), 'vote_count.gte':100, 'sort_by':'vote_average.desc'}
        self.set_discover_params()
        self.get_result_list()
        self.context['data']['top_rated_list'] = self.result_list[:12]

        super().prepare_context_list()


class MoviesPopularView(MoviesListMixin, DiscoverView):
    title = 'Popular'
    view_path = 'movies:popular'
    discover_method = 'discover_movies'
    discover_params = {
        'primary_release_date.lte': time.strftime('%Y-%m-%d'),
        'sort_by': 'popularity.desc'
    }


class MoviesUpcomingView(MoviesListMixin, DiscoverView):
    title = 'Upcoming'
    view_path = 'movies:upcoming'
    discover_method = 'discover_movies'
    discover_params = {
        'primary_release_date.gte': time.strftime('%Y-%m-%d'),
        'sort_by': 'popularity.desc'
    }


class MoviesTopRatedView(MoviesListMixin, DiscoverView):
    title = 'Top Rated'
    view_path = 'movies:top_rated'
    discover_method = 'discover_movies'
    discover_params = {
        'primary_release_date.lte': time.strftime('%Y-%m-%d'),
        'vote_count.gte': 100,
        'sort_by': 'vote_average.desc'
    }


class MoviesSearchView(MoviesListMixin, SearchView):
    title='Search Movies'
    view_path = 'movies:search'

    def get_result_list(self):
        self.result_list = self.prepare_result_list(Movie().search(self.term, self.page))


class MoviesDetailView(MoviesDetailMixin, TmdbDetailView):
    template_name = 'movies/detail.html'
    view_path = 'movies:detail'

    def prepare_context_detail(self):
        self.details = Movie().details(self.id, 'videos,credits')
        self.similar_list = Movie().similar(self.id)
        self.recommendations_list = Movie().recommendations(self.id)
        super().prepare_context_detail()