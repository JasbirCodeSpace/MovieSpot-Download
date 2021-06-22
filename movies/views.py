import json
import logging
import requests
import numpy as np
import pandas as pd
from urllib import parse
import tmdbsimple as tmdb
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from sklearn.metrics.pairwise import linear_kernel,cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer

tmdb.API_KEY = settings.TMDB_API_KEY
# moviesDB = IMDb()

def home(request):
	trending_movies = trending('movie', 'day')
	trending_actors = trending('person', 'day')
	movies = popular_downloads_movies()
	return render(request,'movies/popular-downloads.html',{'nav_home':'active', 'movies': json.loads(movies)})

def popular_downloads(request):
	movies = popular_downloads_movies()
	return render(request, 'movies/popular-downloads.html', {'name_popular': 'active', 'movies': json.loads(movies)})

def latest_downloads(request):
	movies = latest_downloads_movies()
	return render(request, 'movies/latest-downloads.html', {'name_popular': 'active', 'movies': json.loads(movies)})
	
def search_movie2(request, keyword):
	try:
		file_path = settings.BASE_DIR + '/movies/yts_movies.csv'
		fields = ['title', 'small_cover_image' , 'id', 'imdb_code']
		movies = pd.read_csv(file_path, usecols=fields, sep=',')
		
		movies = movies[movies['title'].str.contains(str(keyword),case=False, na=False)]
		movies = movies[:7].copy()
		return JsonResponse({'status': True, 'response': movies.to_json(orient='records')})
	except Exception as e:
		print(e)
		return JsonResponse({'status':False, 'response': 'Something went wrong:('})


def browse_movie(request):
	return render(request,'movies/browse.html',{'nav_browse':'active'})

def movie_recommendation(request):
	return render(request,'movies/recommendation.html',{'nav_recommend':'active', 'movies':[]})

def movie_recommend(request, yts_id):
	movies_count = 15
	movie_id = yts_id
	try:
		output = yts_similar_movies(movie_id, movies_count)
		return JsonResponse({'status':True,'movies':output},safe=False)
	except Exception as e:
		logging.error(e)
		return JsonResponse({'status':False,'error':'Error occured while processing request'},safe=False)


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
				filter['year'].append(filter['year'][0])
			filter['language'] = request.POST.get('movie-language')
			filter['rating'] = request.POST.get('movie-rating')
			required_dict = {'query_term':filter['query_term'],'quality':filter['quality'],'genre':filter['genre'],'sort_by':filter['sort_by'],'limit':50}
			response = requests.get('https://yts.mx/api/v2/list_movies.json',params=required_dict)
			if response:
				movies_response = response.json()
				if movies_response['data']['movie_count']:
					movies_result = movies_response['data']['movies']
					movies = filter_browse_movies(filter, movies_result)
					movies_response['data']['movies'] = movies
					movies_response['data']['movie_count'] = len(movies)
				return JsonResponse({'status':True,'data':movies_response},safe=False)
			else :
				return JsonResponse({'status':False,'error':'No match found'},safe=False)
		except Exception as e:
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
	movie = yts_movie(yts_id)
	if movie:
		movie = movie['data']['movie']
		movie['runtime_hours'] = int(movie['runtime']/60)
		movie['runtime_minutes'] = int(movie['runtime'] % 60)
		movie['genres'] = ', '.join(movie['genres'])
		imdb_response = tmdb_movie(imdb_id)
		if imdb_response:
			movie['poster_path'] = imdb_response['movie_poster']
		else :
			movie['poster_path'] = movie['background_image_original']
		return render(request,'movies/movie.html',{'status':True,'movie':movie})
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

def yts_similar_movies(movie_id, similar_movie_count):
	try:
		file_path = settings.BASE_DIR+'/movies/yts_movies.csv'
		movies = pd.read_csv(file_path,sep=',')
		movie_index = movies[movies.id == int(movie_id)].index

		features = ['genres','title']
		for feature in features:
			movies[feature] = movies[feature].fillna('')

		movies['combined_features'] = movies.apply(combine_features, args=[features], axis=1)
		tfidf = TfidfVectorizer(stop_words='english')
		tfidf_matrix = tfidf.fit_transform(movies['combined_features'])
		cosine_similarity_scores = linear_kernel(tfidf_matrix, tfidf_matrix[movie_index])
		similar_movies = list(enumerate(cosine_similarity_scores))
		similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)
		similar_movies_response = []
		for i in range(1,similar_movie_count+1):
			similar_movies_response.append(get_movie_from_index(movies,similar_movies[i][0]))
		data = json.dumps(similar_movies_response, cls=NpEncoder)
		return data
	except Exception as e:
		logging.error(e)

def popular_downloads_movies(count=30):
	file_path = settings.BASE_DIR + '/movies/yts_movies.csv'
	fields = ['id', 'imdb_code', 'large_cover_image','title', 'year','genres', 'rating']
	movies = pd.read_csv(file_path, usecols=fields, sep=',')
	most_downloaded_movies = movies[:count].copy()
	most_downloaded_movies.loc[:,'genres'] = most_downloaded_movies['genres'].apply(lambda x: ', '.join(x.split()))
	most_downloaded_movies.loc[:,'rating'] = most_downloaded_movies['rating'].apply(lambda x: int(x*10))
	return most_downloaded_movies.to_json(orient='records')

def latest_downloads_movies(count=30):
	file_path = settings.BASE_DIR + '/movies/yts_movies.csv'
	fields = ['id', 'imdb_code', 'large_cover_image','title', 'year','genres', 'rating','date_uploaded']
	movies = pd.read_csv(file_path, usecols=fields, sep=',')

	# latest_downloaded_movies.loc[:,'genres'] = latest_downloaded_movies.loc[:,'genres'].apply(lambda x: ', '.join(x.split()))
	movies.loc[:,'rating'] = movies.loc[:,'rating'].apply(lambda x: int(x*10))
	
	movies.loc[:,'date_uploaded'] = pd.to_datetime(movies['date_uploaded'])
	movies.sort_values(by=['date_uploaded',], ascending=[False], inplace=True)

	latest_downloaded_movies = movies[0:count].copy()
	return latest_downloaded_movies.to_json(orient='records')

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

def trending(media_type, time_window):
	try:
		required_dict = {'api_key': tmdb.API_KEY, 'media_type': media_type, 'time_window': time_window}
		response = requests.get(f'https://api.themoviedb.org/3/trending/{media_type}/{time_window}', params=required_dict)
		return response.json()['results']
	except Exception as e:
		return False

def yts_movie(movie_id,with_images='true',with_cast='true'):
	try:
		required_dict = {'movie_id':movie_id,'with_images':with_images,'with_cast':with_cast}
		response = requests.get('https://yts.mx/api/v2/movie_details.json',timeout=5, params=required_dict)
		return response.json()
	except:
		return False

def filter_browse_movies(filter, movies):
	if filter['rating'] != "all":
		movies = [movie for movie in movies if float(movie['rating']) >= float(filter['rating'])]
	if filter['year'][0] != "all":
		movies = [movie for movie in movies if int(movie['year']) >= int(filter['year'][0]) and int(movie['year'])<=int(filter['year'][1])]
	if filter['language'] != "all":
		movies = [movie for movie in movies if movie['language'] == filter['language']]
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
	result['large_cover_image'] = movie['large_cover_image'].values[0]
	result['rating'] = movie['rating'].values[0]
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

	