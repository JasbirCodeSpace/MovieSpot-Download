from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from imdb import IMDb, IMDbError
import tmdbsimple as tmdb
import requests
from urllib import parse
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

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
	genre_json = genre()
	return JsonResponse(genre_json,safe=False)

def search_movie(request):
	if request.method == 'POST':
		try:
			movie_name = request.POST['movie-name']
			search  = tmdb.Search()
			response = search.movie(query=movie_name)
			return JsonResponse({'data':search.results},safe=False)
		except :
			return JsonResponse({'error':"Error while fetching movie"},safe=False)
	else:
		return JsonResponse({'error':'Only POST requests allowed'},safe=False)
	
def movie(request,yts_id,imdb_id):
	yts_response = yts_movie(yts_id)
	if yts_response:
		yts_response = yts_response['data']['movie']
		yts_response['runtime_hours'] = int(yts_response['runtime']/60)
		yts_response['runtime_minutes'] = int(yts_response['runtime'] % 60)
		imdb_response = tmdb_movie(imdb_id)
		if imdb_response:
			yts_response['movie_image'] = imdb_response['movie_poster']
		else :
			yts_response['movie_image'] = yts_response['background_image_original']

		return render(request,'similar_movies/movie.html',{'status':True,'data':yts_response})
	else:
		return render(request,'similar_movies/movie.html',{'status':False,'error':'Movie not found'})

def similar_movies(request):
	file_path = settings.BASE_DIR+'/similar_movies/yts_movies.csv'
	df = pd.read_csv(file_path,sep=',')

	features = ['title','genres']
	for feature in features:
		df[feature] = df[feature].fillna('')

	df['combined_features'] = df.apply(combine_features,args=[features],axis=1)

	cv = CountVectorizer()
	count_matrix = cv.fit_transform(df['combined_features'])
	cosine_similarity_scores = cosine_similarity(count_matrix)
	movie_id = '18414'
	movie_row = df[df.id == movie_id].values[0]
	print(movie_row)


	return HttpResponse(request,'here')

# =========================================================================================
# Helper methods
# ========================================================================================
def genre():
	response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=' +  tmdb.API_KEY + '&language=en-US')
	return response.json()


def tmdb_movie(imdb_id):
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

		return movie_data
	except :
		return False

	
def yts_movie(movie_id,with_images='true',with_cast='true'):
	try:
		required_dict = {'movie_id':movie_id,'with_images':with_images,'with_cast':with_cast}
		response = requests.get('https://yts.mx/api/v2/movie_details.json',params=required_dict)
		return response.json()
	except:
		return False

def combine_features(row,features):
	try:
		combined_data = ""
		for feature in features:
			combined_data += row[feature] + " " 
		return combined_data
	except Exception as e:
		return combined_data

