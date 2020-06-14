from django.urls import path
from . import views

urlpatterns = [
	path('',views.home,name='movie-home'),
	path('search-movie',views.search_movie,name='search-movie'),
	path('get-genre',views.get_genre,name='get-genre'),
	path('browse-movie',views.browse_movie,name='browse-movie')
]