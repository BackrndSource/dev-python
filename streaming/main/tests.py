from django.test import TestCase, Client
from django.conf import settings
from .views import TmdbView, TmdbListView, MoviesSearchView, SeriesSearchView

class TMDbTests(TestCase):
	def setUp(self):
		self.tmdb_view = TmdbView()
		self.tmdb_view.tmdb_set_up()

	def test_tmdb_set_up(self):
		self.assertEqual(self.tmdb_view.tmdb.api_key, settings.TMDB_API_KEY)
		self.assertEqual(self.tmdb_view.tmdb.language, settings.TMDB_API_LANG)
		self.assertEqual(self.tmdb_view.tmdb.debug, settings.TMDB_API_DEBUG)

	def test_TmdbListView(self):
		view = TmdbListView()
		view.paginate = True
		view.page = 3
		view.prepare_context_list()
		self.assertEqual(view.context['data']['pagination'][0], 1)
		self.assertEqual(view.context['data']['next_page'], 4)
		self.assertEqual(view.context['data']['prev_page'], 2)
		view.page = 1
		view.prepare_context_list()
		self.assertEqual(view.context['data']['pagination'][0], 1)
		self.assertEqual(view.context['data']['next_page'], 2)
		self.assertEqual(view.context['data']['prev_page'], None)
