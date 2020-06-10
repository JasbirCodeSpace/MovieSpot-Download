from django.shortcuts import render

def home(request):
	return render(request,'similar_movies/index.html')
