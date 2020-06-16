from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from imdb import IMDb, IMDbError
import tmdbsimple as tmdb
import requests
from urllib import parse

moviesDB = IMDb()
tmdb.API_KEY = 'a25592d6509c51f48ff31ed09207fbaf'

def home(request):
	return render(request,'similar_movies/index.html')

def browse_movie(request):
	return render(request,'similar_movies/browse.html')

def browse_movie_form(request):
	if request.method == 'POST':

		query_term = request.POST.get('movie-name')
		quality = request.POST.get('movie-quality')
		genre = request.POST.get('movie-genre')
		sort_by = request.POST.get('movie-order')
		year = request.POST.get('movie-year')
		language = request.POST.get('movie-language')

		required_dict = {'query_term':query_term,'quality':quality,'genre':genre,'sort_by':sort_by,'limit':50}
		response = requests.get('https://yts.mx/api/v2/list_movies.json',params=required_dict)
		if response:
			return JsonResponse({'status':True,'data':response.json()},safe=False)
		else :
			return JsonResponse({'status':False,'error':response.json()},safe=False)

	return JsonResponse({'status':False,'error':'Invalid Request'},safe=False)

	
def get_genre(request):
	response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=' +  tmdb.API_KEY + '&language=en-US')
	return JsonResponse(response.json(),safe=False)
def search_movie(request):
	if request.method == 'POST':
		try:
			movie_name = request.POST['movie-name']
			search  = tmdb.Search()
			response = search.movie(query=movie_name)
			# print(search.genre())
			return JsonResponse({'data':search.results},safe=False)
		except :
			return JsonResponse({'error':"Error while fetching movie"},safe=False)
	else:
		return JsonResponse({'error':'Only POST requests allowed'},safe=False)

def movie(request,movie_id):
	try:
		required_dict = {'api_key':tmdb.API_KEY,'external_source':'imdb_id'}
		if len(movie_id) == 9:
			new_movie_id = movie_id[2:]
		else:
			new_movie_id = movie_id[2:]
		response = requests.get(f'https://api.themoviedb.org/3/find/{movie_id}',params=required_dict)
# https://image.tmdb.org/t/p/original/lz1qjw1wDbE2Kj76iTXpGKQSPKD.jpg
		return render(request,'similar_movies/movie.html',{'status':True,'data':response.json()})
	except :
		return render(request,'similar_movies/movie.html',{'status':False,'error':'Movie not found'})