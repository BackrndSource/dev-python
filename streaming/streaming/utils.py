from django.conf import settings
from tmdbv3api import TMDb, Genre
from urllib.parse import quote
from django.utils.encoding import iri_to_uri
import requests
import unicodedata

def is_invalid_page(page):
    if page < 1 or page > 500:
        return True;
    return False;

def tmdb_activate():
    tmdb = TMDb()
    tmdb.api_key = settings.TMDB_API_KEY
    tmdb.language = settings.TMDB_API_LANG
    tmdb.debug = settings.TMDB_API_DEBUG

def prepare_movies_result_list(item_list):
    '''
    Return edited version of default response given by Tmdbv3api
    '''
    for i, s in enumerate(item_list):
        #Adding URL to poster_path
        if hasattr(item_list[i], 'poster_path'):
            if s.poster_path != '' and s.poster_path != None:
                if s.poster_path.find('https://image.tmdb.org/t/p/') == -1:
                    item_list[i].poster_path = 'https://image.tmdb.org/t/p/w500' + s.poster_path
                else:
                    item_list[i].poster_path = 'img/no_poster.png'
            else:
                item_list[i].poster_path = 'img/no_poster.png'

        #Split release_date to get Year
        if hasattr(item_list[i], 'release_date'):
            item_list[i].release_year = s.release_date.split('-', 1)[0]
        
        #Creating URL Slug
        if hasattr(item_list[i], 'title'):
            item_list[i].slug = quote(s.title.lower().encode('ascii', 'ignore').decode().replace('  ', '').replace(':', ''))
            
    return item_list

def prepare_context(type, title='', tmdb_response=None, page=None, limit=99, load_genre_list=True):
    result_list = None
    genre_list = None

    if load_genre_list:
        #Set in context['data']['genre_list']
        genre = Genre()
        if type == "movies":
            genre_list = genre.movie_list()
        if type == "series":
            genre_list = genre.tv_list()

    if tmdb_response != None: 
        #Prepare response to set in context['data']['result_list']
        if type == 'movies':
            result_list = prepare_movies_result_list(tmdb_response[:limit])
        if type == 'series':
            result_list = None

    context = {'data': {
        'type': type,
        'title': title,
        'genre_list': genre_list,
        'result_list': result_list
    }}

    if page != None: 
        #Activate pagination
        pagination = list()
        if page < 5:
            for x in range(1,10):
                pagination.append(x)
        elif page > 495:
            for x in range(492,501):
                pagination.append(x)
        else:
            for x in range(page - 4, page):
                pagination.append(x)
            for x in range(page, page + 5):
                pagination.append(x)

        next_page = page + 1
        prev_page = page - 1

        if page == 1:
            prev_page = None
        if page == 500:
            next_page = None

        context['data']['page'] = page
        context['data']['pagination'] = pagination
        context['data']['next_page'] = next_page
        context['data']['prev_page'] = prev_page

    return context
