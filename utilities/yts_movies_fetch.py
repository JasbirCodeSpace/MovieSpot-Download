import requests
import csv

def yts_movies():
	# try:
		yts_movies = []
		required_dict = {'limit':50,'page':1,'sort_by':'download_count'}
		response = requests.get('https://yts.mx/api/v2/list_movies.json',params=required_dict)
		response = response.json()['data']
		num_pages = int(response['movie_count']/response['limit'])+1
		yts_movies = response['movies']

		for page in range(2,num_pages+1):
			print(page)
			required_dict = {'limit':50,'page':page}
			response = requests.get('https://yts.mx/api/v2/list_movies.json',params=required_dict)
			response = response.json()['data']
			if 'movies' in response:
				yts_movies = yts_movies + response['movies']
			else:
				print(page)
				print(response)
		columns = ['id', 'url', 'imdb_code', 'title', 'title_english', 'title_long', 'slug', 'year', 'rating', 'runtime', 'genres', 'summary', 'description_full', 'synopsis', 'yt_trailer_code', 'language', 'mpa_rating', 'background_image', 'background_image_original', 'small_cover_image', 'medium_cover_image', 'large_cover_image', 'state', 'torrents', 'date_uploaded', 'date_uploaded_unix']
		write_to_csv(yts_movies,columns)
	# except Exception as e:
	# 	print(e)

def write_to_csv(data,columns):
	csv_file = 'yts_movies.csv'
	try:
		with open(csv_file,'w',encoding="utf-8") as csvfile:
			writer = csv.DictWriter(csvfile,fieldnames=columns)
			writer.writeheader()
			for movie in data:
				if 'genres' in movie:
					movie['genres'] = '  '.join(movie['genres'])
				writer.writerow(movie)
	except IOError:
		print("error")


yts_movies()