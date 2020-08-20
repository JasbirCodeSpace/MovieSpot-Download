import requests
import pandas as pd
import csv
import cfscrape
scraper = cfscrape.create_scraper()

yts_movies_details = []
urls = []
counter = 0
columns = ['id', 'url', 'imdb_code', 'title', 'title_english', 'title_long', 'slug', 'year',
    'rating', 'runtime', 'genres', 'download_count', 'like_count', 'description_intro',
    'description_full', 'yt_trailer_code', 'language', 'mpa_rating', 'background_image',
    'background_image_original', 'small_cover_image', 'medium_cover_image', 'large_cover_image',
    'medium_screenshot_image1', 'medium_screenshot_image2', 'medium_screenshot_image3',
    'large_screenshot_image1', 'large_screenshot_image2', 'large_screenshot_image3', 'cast', 'torrents',
    'date_uploaded', 'date_uploaded_unix']

def yts_movie_detail():

    yts_movies = pd.read_csv('yts_movies.csv')


    for id in yts_movies['id']:
        url = f'https://yts.mx/api/v2/movie_details.json?movie_id={id}&with_images=false&with_cast=true'
        urls.append(url)

    for url in urls:
        response = requests.get(url)
        print(response)
        print(url)
        response = response.json()['data']['movie']
        response['genres'] = ' '.join(response['genres'])
        yts_movies_details.append(response)
        counter = counter + 1
        print(counter)
    


    write_to_csv(yts_movies_details, columns)

def write_to_csv(data, columns):
    csv_file = 'yts_movies_details.csv'
    try:
        with open(csv_file, 'w', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            for movie in data:
                writer.writerow(movie)
    except Exception as e:
        print(e)

yts_movie_detail()
