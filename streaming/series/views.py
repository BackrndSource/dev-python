from tmdbv3api import TV, Discover, Genre
from main.views import DiscoverView, TmdbDetailView, SearchView
import time

class SeriesListMixin():

    def get(self, request, *args, **kwargs):
        self.genre_list = Genre().tv_list()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.genre_list = Genre().tv_list()
        return super().post(request, *args, **kwargs)


class SeriesHomeView(SeriesListMixin, DiscoverView):
    title = 'Series Home'
    view_path = 'series:home'
    paginate = False
    template_name = 'main/home.html'
    discover_method = 'discover_tv_shows'

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


class SeriesPopularView(SeriesListMixin, DiscoverView):
    title = 'Popular Series'
    view_path = 'series:popular'
    discover_method = 'discover_tv_shows'
    discover_params = {
        'primary_release_date.lte': time.strftime('%Y-%m-%d'),
        'sort_by': 'popularity.desc'
    }


class SeriesUpcomingView(SeriesListMixin, DiscoverView):
    title = 'Upcoming Series'
    view_path = 'series:upcoming'
    discover_method = 'discover_tv_shows'
    discover_params = {
        'primary_release_date.gte': time.strftime('%Y-%m-%d'),
        'sort_by': 'popularity.desc'
    }


class SeriesTopRatedView(SeriesListMixin, DiscoverView):
    title = 'Top Rated Series'
    view_path = 'series:top_rated'
    discover_method = 'discover_tv_shows'
    discover_params = {
        'primary_release_date.lte': time.strftime('%Y-%m-%d'),
        'vote_count.gte': 100,
        'sort_by': 'vote_average.desc'
    }


class SeriesSearchView(SeriesListMixin, SearchView):
    title='Search Series'
    view_path = 'series:search'

    def get_result_list(self):
        self.result_list = self.prepare_result_list(TV().search(self.term, self.page))


class SeriesDetailView(TmdbDetailView):
    template_name = 'series/detail.html'
    view_path = 'series:detail'

    def get_result_detail(self):
        return TV().details(self.id, 'append_to_response=videos,credits')