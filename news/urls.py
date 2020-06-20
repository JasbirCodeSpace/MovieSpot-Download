from django.urls import path
from . import views

urlpatterns = [
	path('movies',views.movies_news,name='movies-news'),
	path('actors',views.actors_news,name='actors-news')
]