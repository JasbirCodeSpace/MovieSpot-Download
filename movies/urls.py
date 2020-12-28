from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='home'),
	path('search-movie',views.search_movie,name='search-movie'),
	path('get-genre',views.get_genre,name='get-genre'),
	path('browse-movie',views.browse_movie,name='browse-movie'),
	path('browse-movie-form',views.browse_movie_form,name='browse-movie-form'),
	path('movie/<str:yts_id>/<str:imdb_id>',views.movie,name='movie'),
	path('similar-movies',views.similar_movies,name='similar-movies'),
	path('movie-recommendation',views.movie_recommendation,name='movie-recommendation'),
	path('movie-recommend/<str:yts_id>', views.movie_recommend, name='movie-recommend'),
	path('popular-downloads', views.popular_downloads, name='popular-downloads'),
	path('latest-downloads', views.latest_downloads, name='latest-downloads'),
	path('search-movie/<str:keyword>', views.search_movie2, name='search-movie'),
]