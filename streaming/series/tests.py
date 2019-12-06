from django.test import TestCase, Client
from main.views import TmdbView

class SeriesTests(TestCase):
	def setUp(self):
		self.tmdb_view = TmdbView()
		self.tmdb_view.tmdb_set_up()

	def test_movies_discover_views(self):
		url_paths = ['/series/popular/','/series/upcoming/','/series/top_rated/']

		for url_path in url_paths:
			response = self.client.get('%s?genre=18,6sd8,45,fgtyh,899' % url_path)
			self.assertTrue(len(response.context['data']['result_list']) == 0)
			self.assertEqual(response.context['data']['genre_active_list'][0], 18)
			self.assertEqual(response.context['data']['genre_active_list'][1], 45)
			self.assertEqual(response.context['data']['genre_active_list'][2], 899)

			response = self.client.get('%s?genre=' % url_path)
			self.assertTrue(len(response.context['data']['result_list']) > 1)
			self.assertEqual(response.context['data']['genre_active_list'], None)
			self.assertTrue(response.context['data']['pagination'][0] == 1)
			self.assertTrue(response.context['data']['pagination'][8] == 9)

			response = self.client.get('%s10/' % url_path)
			self.assertTrue(len(response.context['data']['result_list']) > 1)
			self.assertTrue(response.context['data']['pagination'][0] == 6)
			self.assertTrue(response.context['data']['pagination'][8] == 14)

			response = self.client.get('%s' % url_path)
			self.assertTrue(len(response.context['data']['result_list']) > 1)
			print('%s:' % url_path)
			print(response.context['data']['result_list'][:5])



