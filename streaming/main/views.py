from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from tmdbv3api import TMDb, Genre, Discover, Movie, TV, Collection
from tmdbv3api.as_obj import AsObj
from urllib.parse import quote
from sites.models import *
import time
import unidecode
import re

class TmdbView(View):

	tmdb = TMDb()

	#context
	title = ''
	view_path = ''
	genre_list = None

	template_name = 'main/base.html'

	context = {'data':{}}

	def dispatch(self, request, *args, **kwargs):
		self.context = {'data':{}} # Clean parameter. If not, context will be charged with the data of the last call ?¿
		self.tmdb_set_up()
		return super(TmdbView, self).dispatch(request, *args, **kwargs)

	def tmdb_set_up(self):
		self.tmdb.api_key = settings.TMDB_API_KEY
		self.tmdb.language = settings.TMDB_API_LANG
		self.tmdb.debug = settings.TMDB_API_DEBUG

	def get(self, request):
		self.prepare_context()
		return render(request, self.template_name, self.context)

	def prepare_context(self):
		self.context['data']['title'] = self.title
		self.context['data']['view_path'] = self.view_path
		self.context['data']['view_path_base'] = self.view_path.split(':')[0]
		self.context['data']['genre_list'] = self.genre_list

	def prepare_result_list(self, result_list):
		'''
		Edit default list response given by Tmdbv3api. Movies, Tv and People.

		From: <List> of <dict> items
		To: <List> of <tmdbv3api.AsObj> edited items

		'''
		if result_list:
			for k,item in enumerate(result_list): 
				if not isinstance(item, AsObj):
					result_list[k] = AsObj(**item)

			for item in result_list:
				self.parse_tmdb_item(item)

		return result_list

	def parse_tmdb_item(self, item):
		'''
		Adds to item:
			- poster_url_w500
			- release_year
			- slug
		 	- subtitle
		'''
		# Series
		if hasattr(item, 'first_air_date'):
			item.release_date = item.first_air_date
		if hasattr(item, 'name'):
			item.title = item.name

		# People
		if hasattr(item, 'profile_path'):
			item.poster_path = item.profile_path
		if hasattr(item, 'character'):
			item.subtitle = item.character
		if hasattr(item, 'department'):
			item.subtitle = item.department

		# Movies/Series/People
		if hasattr(item, 'poster_path'):
			item.poster_url_w500 = self.get_poster_url_w500(item.poster_path)
		if hasattr(item, 'title'):
			item.slug = re.sub('[^A-z0-9\s]','',unidecode.unidecode(item.title)).lower().replace('  ', ' ').replace(' ', '-')
		if hasattr(item, 'release_date'):
			item.release_year = item.release_date.split('-', 1)[0]

	def get_poster_url_w500(self, poster_path):
		if poster_path != None:
			return 'https://image.tmdb.org/t/p/w500' + poster_path
		else:
			return self.get_no_poster_url_w500()

	@staticmethod
	def get_no_poster_url_w500():
		return 'img/no_poster.png'

	def getBackdropCssStyle(self, backdrop_path):
		if backdrop_path != '':
			return 'background-image:url(' + self.getBackdropUrl(backdrop_path) + ')'
		else:
			return 'background-color:#4e4e4e'

	@staticmethod
	def getBackdropUrl(backdrop_path):
		if backdrop_path != '':
			return 'https://image.tmdb.org/t/p/original' + backdrop_path


class TmdbDetailView(TmdbView):
	id = None
	template_name = 'main/detail.html'

	#context
	details = None
	site_list = None
	collection = None
	similar_list = None
	recommendations_list = None

	def get(self, request, id, slug = None):
		self.id = id

		#if self.is_invalid_id():
		#	return redirect(reverse(self.view_path))

		return super().get(request)

	def prepare_context(self):
		self.prepare_context_detail()
		super().prepare_context()

	def prepare_context_detail(self):
		self.context['data']['details'] = self.prepare_result_detail(self.details)
		self.prepare_context_sites()
		self.context['data']['site_list'] = self.site_list
		self.prepare_context_collection()
		self.context['data']['collection'] = self.collection
		
		if self.similar_list:
			self.context['data']['similar_list'] = self.prepare_result_list(self.similar_list)[:12]
		if self.recommendations_list:
			self.context['data']['recommendations_list'] = self.prepare_result_list(self.recommendations_list)[:12]

	def prepare_result_detail(self, details):
		'''
		Return edited version of default response given by Tmdbv3api.

		Adds:
			- backdrop_css
			- poster_url_w500
			- trailer_url
			- trailer_embed
		'''
		self.parse_tmdb_item(details)

		if hasattr(details, 'backdrop_path'):
			if details.backdrop_path != '' and details.backdrop_path != None:
				details.backdrop_css = self.getBackdropCssStyle(details.backdrop_path)

		if hasattr(details, 'videos'):
			if details.videos['results']:
				if details.videos['results'][0]['site'] == 'YouTube':
					details.trailer_url = 'https://www.youtube.com/watch?v=' + details.videos['results'][0]['key']
					details.trailer_embed = 'https://www.youtube.com/embed/' + details.videos['results'][0]['key']

		if hasattr(details, 'credits'):
			if details.credits['cast']:
				self.prepare_result_list(details.credits['cast'])[:18]

			if details.credits['crew']:
				self.prepare_result_list(details.credits['crew'])[:18]
		
		return details

	def prepare_context_sites(self):
		self.site_list = Site.objects.all()

		for site in self.site_list:
			# Compose the urls for the sites
			if hasattr(self.details, 'title'):
				site.search_url = site.get_search_url(self.details.title)
			elif hasattr(self.details, 'name'):
				site.search_url = site.get_search_url(self.details.name)

	def prepare_context_collection(self):
		if hasattr(self.details, 'belongs_to_collection'):
			if self.details.belongs_to_collection:
				collection = Collection().details(self.details.belongs_to_collection['id'])
				if collection.parts:
					self.prepare_result_list(collection.parts)
				if collection.backdrop_path:
					collection.backdrop_style = self.getBackdropCssStyle(collection.backdrop_path)
				self.collection = collection


class TmdbListView(TmdbView):
	
	template_name = 'main/list.html'

	result_list = None
	result_list_limit = 99

	#context
	genre_active_list = None

	#paginator
	page = 1
	page_max = 500
	paginate = False

	def get(self, request, page = 1):
		self.page = page

		if self.is_invalid_page():
			return redirect(reverse(self.view_path))

		if request.GET.get('genre'):
			# Only int accepted, that correspond to id_genre. 
			# Param: ?genre=id,id2,id3...
			self.genre_active_list = list()
			for id_genre in request.GET.get('genre').split(','):
				try:
					self.genre_active_list.append(int(id_genre))
				except ValueError:
					pass
			if len(self.genre_active_list)<1:
				self.genre_active_list = None

		return super().get(request)

	def is_invalid_page(self):
		if self.page < 1 or self.page > self.page_max:
			return True;
		return False;

	def prepare_context(self):
		self.prepare_context_list()
		super().prepare_context()

	def prepare_context_list(self):
		self.get_result_list()
		self.context['data']['result_list'] = self.result_list
		self.context['data']['genre_active_list'] = self.genre_active_list

		if self.paginate == True:
			self.prepare_context_pagination()

	def get_result_list(self):
		self.result_list = None

	def prepare_context_pagination(self):
		pagination = list()
		if self.page < 5:
			for x in range(1,10):
				pagination.append(x)
		elif self.page > 495:
			for x in range(492,501):
				pagination.append(x)
		else:
			for x in range(self.page - 4, self.page):
				pagination.append(x)
			for x in range(self.page, self.page + 5):
				pagination.append(x)

		next_page = self.page + 1
		prev_page = self.page - 1

		if self.page == 1:
			prev_page = None
		if self.page == 500:
			next_page = None

		self.context['data']['page'] = self.page
		self.context['data']['pagination'] = pagination
		self.context['data']['next_page'] = next_page
		self.context['data']['prev_page'] = prev_page


class DiscoverView(TmdbListView):
	discover_params = {}
	paginate = True

	def prepare_context_list(self):
		self.set_discover_params()
		super().prepare_context_list()
	
	def set_discover_params(self):
		self.discover_params['page'] = self.page
		self.discover_params.pop('with_genres', None)
		
		if self.genre_active_list:
			self.discover_params['with_genres'] = ','.join(map(str, self.genre_active_list))

	def get_result_list(self):
		self.result_list = self.prepare_result_list(getattr(Discover(), self.discover_method)(self.discover_params))[:self.result_list_limit]


class SearchView(TmdbListView):
	term = None

	template_name = 'main/search.html'

	def post(self, request):
		self.term = request.POST.get('term')

		if request.POST.get('page'):
			try:
				self.page = int(request.POST.get('page'))
			except ValueError:
				return redirect(reverse(self.view_path))

		if self.is_invalid_page():
			return redirect(reverse(self.view_path))

		self.tmdb_set_up()
		self.prepare_context()

		return render(request, self.template_name, self.context)

	def get(self, request):
		self.tmdb_set_up()
		self.prepare_context()
		return render(request, self.template_name, self.context)

	def prepare_context_list(self):
		if self.term != None and self.term != '':
			self.context['data']['term'] = self.term
			self.paginate = True
			super().prepare_context_list()