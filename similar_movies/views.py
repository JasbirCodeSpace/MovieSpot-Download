from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from imdb import IMDb, IMDbError

moviesDB = IMDb()
def home(request):
	# moviesDB = imdb.IMDb()
	# movies = moviesDB.search_movie('inception')
	# for movie in movies:
	# 	title = movie['title']
	# 	year = movie['year']
	# 	print(f'{title} :{year}')
	# id = movies[0].getID()
	# movie = moviesDB.get_movie(id)
	# print(movie['title'],movie['year'],movie['cast'],movie['rating'],movie['directors'])
	return render(request,'similar_movies/index.html')

def search_movie(request):
	if request.method == 'POST':
		movie_name = request.POST['movie-name']
		try:
			movies = moviesDB.search_movie(movie_name)
			movieList = []
			for movie in movies:
				id = movie.movieID
				current_movie = moviesDB.get_movie(id)

				title = current_movie['title']
				cast = ', '.join(map(str,current_movie['cast']))
				directors = ', '.join(map(str,current_movie['directors']))
				year = current_movie['year']
				plot = current_movie['plot']
				rating = current_movie['rating']
				# movieList.append([title,year,rating,cast,directors])
			# print(movieList)

		except IMDbError as e:
			return JsonResponse({'error':e},safe=False)	

		return JsonResponse({'data':'here'},safe=False)
	else:
		return JsonResponse({'error':'Only POST requests allowed'},safe=False)