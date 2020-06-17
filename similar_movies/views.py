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

def genre():
	response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=' +  tmdb.API_KEY + '&language=en-US')
	return response.json()

def get_genre(request):
	genre_json = genre()
	return JsonResponse(genre_json,safe=False)

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

def movie(request,yts_id,imdb_id):
	try:
		required_dict = {'api_key':tmdb.API_KEY,'external_source':'imdb_id'}
		if len(imdb_id) == 9:
			new_movie_id = imdb_id[2:]
		else:
			new_movie_id = imdb_id
		response = requests.get(f'https://api.themoviedb.org/3/find/{imdb_id}',params=required_dict)
		json_response = response.json()['movie_results'][0]

		movie_data = {}
		movie_data['movie_name'] = json_response['title']
		movie_data['movie_poster'] = 'https://image.tmdb.org/t/p/original/'+json_response['poster_path']
		movie_data['rating'] = json_response['vote_average']
		movie_data['language'] = json_response['original_language']
		movie_data['release_date'] = json_response['release_date']

		if movie_data['release_date']!='' and movie_data['release_date'].find('-')!=-1:
			movie_data['release_date'] = movie_data['release_date'].split('-')[0]

		movie_data['overview'] = json_response['overview']

		# genre mapping 
		genre_json = genre()['genres']
		genre_mapping = {}
		movie_data['genre'] = []
		for x in genre_json:
			genre_mapping[x['id']] = x['name']

		for genre_id in json_response['genre_ids']:
			movie_data['genre'].append(genre_mapping[genre_id])
		movie_data['genre'] = ' / '.join(movie_data['genre'])
		# end of genre mapping 

		return render(request,'similar_movies/movie.html',{'status':True,'data':movie_data})
	except :
		return render(request,'similar_movies/movie.html',{'status':False,'error':'Movie not found'})