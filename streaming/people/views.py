from django.shortcuts import render, redirect
from django.urls import reverse
from tmdbv3api import Person, Movie
from main.views import TmdbDetailView, SearchView, TmdbListView


class PeopleListMixin():

	def get(self, request, *args, **kwargs):
		return super().get(request, *args, **kwargs)


class PeopleSearchView(PeopleListMixin, SearchView):
	title='Search People'
	view_path = 'people:search'

	def get_result_list(self):
		self.result_list = self.prepare_result_list(Person().search(self.term, self.page))


class PeoplePopularView(PeopleListMixin, TmdbListView):
	title='Popular People'
	view_path = 'people:popular'

	def get_result_list(self):
		self.result_list = self.prepare_result_list(Person().popular(self.page))


class PeopleDetailView(TmdbDetailView):
	template_name = 'people/detail.html'
	view_path = 'people:detail'

	def prepare_context_detail(self):
		self.details = Person().details(self.id)
		super().prepare_context_detail()