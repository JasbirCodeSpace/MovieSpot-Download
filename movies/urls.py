from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='movie-home'),
	path('search-movie',views.search_movie,name='search-movie'),
	path('get-genre',views.get_genre,name='get-genre'),
	path('browse-movie',views.browse_movie,name='browse-movie'),
	path('browse-movie-form',views.browse_movie_form,name='browse-movie-form'),
	path('movie/<str:yts_id>/<str:imdb_id>',views.movie,name='movie'),
	path('similar-movies',views.similar_movies,name='similar-movies'),
	path('movie-recommendation',views.movie_recommendation,name='movie-recommendation'),
	path('movie-recommend',views.movie_recommend,name='movie-recommend')
]