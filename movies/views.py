from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from imdb import IMDb, IMDbError
import tmdbsimple as tmdb
import requests
from urllib import parse
import pandas as pd
import numpy as np
import json
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
from django.views.decorators.csrf import csrf_exempt

moviesDB = IMDb()
tmdb.API_KEY = 'a25592d6509c51f48ff31ed09207fbaf'

def home(request):
	return render(request,'movies/index.html',{'nav_home':'active'})

def browse_movie(request):
	return render(request,'movies/browse.html',{'nav_browse':'active'})

def movie_recommendation(request):
	return render(request,'movies/recommendation.html',{'nav_recommend':'active'})

def movie_recommend(request):
	if request.method == 'POST':
		# try:
			movie_name = request.POST.get('movie-name')
			sort_by = 'rating'
			limit = 1
			required_dict = {'query_term':movie_name,'sort_by':sort_by,'limit':limit}
			response = requests.get('https://yts.mx/api/v2/list_movies.json',params=required_dict)
			if response:
				response = response.json()['data']
				if(response['movie_count'] > 0 and 'movies' in response):
					movie = response['movies'][0]
					movie_id = movie['id']
					movie_imdb_code = movie['imdb_code']
					output = yts_similar_movies(movie_id,25)
					return JsonResponse({'status':True,'data':output},safe=False)
				else:
					return JsonResponse({'status':False,'error':'No match found'},safe=False)
			else:
				return JsonResponse({'status':False,'error':'No match found'},safe=False)
		# except Exception as e:
		# 	return JsonResponse({'status':False,'error':'Error occured while processing request'},safe=False)
	else:
		return JsonResponse({'status':False,'error':'Invalid Request'})


def browse_movie_form(request):
	if request.method == 'POST':
		try:
			filter = {}
			filter['query_term'] = request.POST.get('movie-name')
			filter['quality'] = request.POST.get('movie-quality')
			filter['genre'] = request.POST.get('movie-genre')
			filter['sort_by'] = request.POST.get('movie-order')
			filter['year'] = request.POST.get('movie-year').split('-')
			if len(filter['year']) == 1:
				filter['year'][1] = filter['year'][0]

			filter['language'] = request.POST.get('movie-language')
			filter['movie-rating'] = request.POST.get('movie-rating')
			required_dict = {'query_term':filter['query_term'],'quality':filter['quality'],'genre':filter['genre'],'sort_by':filter['sort_by'],'limit':50}
			response = requests.get('https://yts.mx/api/v2/list_movies.json',params=required_dict)
			if response:
				movies_response = response.json()
				if movies_response['data']['movie_count']:
					movies_result = movies_response['data']['movies']
					movies = filter_browse_movies(filter, movies_result)
					print(len(movies))
					movies_response['data']['movies'] = movies
				return JsonResponse({'status':True,'data':movies_response},safe=False)
			else :
				return JsonResponse({'status':False,'error':'No match found'},safe=False)
		except:
			return JsonResponse({'status':False,'error':'Error occured while processing request'},safe=False)

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

		return render(request,'movies/movie.html',{'status':True,'data':yts_response})
	else:
		return render(request,'movies/movie.html',{'status':False,'error':'Movie not found'})

@csrf_exempt
def similar_movies(request):
	if request.method == 'POST':
		try:
			movie_id = int(request.POST.get('movie_id'))
			similar_movie_count = int(request.POST.get('movie_count'))
			response = yts_similar_movies(movie_id,similar_movie_count)
			return JsonResponse({'status':True,'data':response},safe=False)
		except:
			return JsonResponse({'status':False,'error':"Error while processing requests"})
	else:
		return JsonResponse({'status': False, 'error': 'Invalid Request'})

# =========================================================================================
# Helper methods
# ========================================================================================
def genre():
	response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=' +  tmdb.API_KEY + '&language=en-US')
	return response.json()

def yts_similar_movies(movie_id,similar_movie_count):
	file_path = settings.BASE_DIR+'/movies/yts_movies.csv'
	movies = pd.read_csv(file_path,sep=',')
	movie_index = movies[movies.id == movie_id].index

	features = ['genres','title']
	for feature in features:
		movies[feature] = movies[feature].fillna('')

	movies['combined_features'] = movies.apply(combine_features,args=[features],axis=1)
	tfidf = TfidfVectorizer(stop_words='english')
	tfidf_matrix = tfidf.fit_transform(movies['combined_features'])

	cosine_similarity_scores = linear_kernel(tfidf_matrix,tfidf_matrix[movie_index])
	similar_movies = list(enumerate(cosine_similarity_scores))
	similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
	similar_movies_response = []
	for i in range(1,similar_movie_count+1):
		similar_movies_response.append(get_movie_from_index(movies,similar_movies[i][0]))
	data = json.dumps(similar_movies_response, cls=NpEncoder)
	return data


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

def filter_browse_movies(filter, movies):
	if filter['rating'] != "all":
		movies = [movie for movie in movies if movie['rating'] >= filter['rating']]
	if filter['year'][0] != "all":
		movies = [movie for movie in movies if movie['year'] >= filter['year'][0] and movie['year']<=filter['year'][1]]
	if filter['language'] != "all":
		movies = [movie for movie in movies if movie['language'] == filter['language']]
	print(movies)
	return movies

def combine_features(row,features):
	try:
		combined_data = ""
		for feature in features:
			combined_data += row[feature] + " " 
		return combined_data
	except Exception as e:
		return combined_data

def get_movie_from_index(df,index):
	movie = df[df.index == index]
	result = {}
	result['id'] = movie['id'].values[0]
	result['imdb_code'] = movie['imdb_code'].values[0]
	result['title'] = movie['title'].values[0]
	result['year'] = movie['year'].values[0]
	result['medium_cover_image'] = movie['medium_cover_image'].values[0]
	return result

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NpEncoder, self).default(obj)