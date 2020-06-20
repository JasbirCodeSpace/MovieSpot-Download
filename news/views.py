from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
import requests
from bs4 import BeautifulSoup

def movies_news(request):
	return HttpResponse(request,'<h1>Movies News</h1>')

def actors_news(request):
	return HttpResponse(request,'<h1>Actors News</h1>')
