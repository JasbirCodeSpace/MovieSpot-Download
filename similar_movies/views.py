from django.shortcuts import render
import imdb

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
