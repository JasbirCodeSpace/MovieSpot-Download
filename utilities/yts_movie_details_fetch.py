import requests
import pandas as pd
import csv
import aiohttp
import asyncio

yts_movies_details = []
urls = []
columns = ['id', 'url', 'imdb_code', 'title', 'title_english', 'title_long', 'slug', 'year',
'rating', 'runtime', 'genres', 'download_count', 'like_count', 'description_intro',
'description_full', 'yt_trailer_code', 'language', 'mpa_rating', 'background_image',
'background_image_original', 'small_cover_image', 'medium_cover_image', 'large_cover_image',
'medium_screenshot_image1', 'medium_screenshot_image2', 'medium_screenshot_image3',
'large_screenshot_image1', 'large_screenshot_image2', 'large_screenshot_image3', 'cast', 'torrents',
'date_uploaded', 'date_uploaded_unix']

async def fetch(session, url, idx):
    async with session.get(url) as response:
        json_response = await response.json()
        yts_movies_details.append(json_response['data']['movie'])
        print(idx)


def prepare_urls():

    yts_movies = pd.read_csv('yts_movies.csv')
    # yts_movies = yts_movies[:10000]

    for id in yts_movies['id']:
        url = f'https://yts.mx/api/v2/movie_details.json?movie_id={id}&with_images=false&with_cast=true'
        urls.append(url)
    # for id in yts_movies['id']:
    #     required_dict = {'movie_id': id, 'with_images': 'false', 'with_cast': 'true'}
    #     response = requests.get('https://yts.mx/api/v2/movie_details.json', params=required_dict)
    #     response = response.json()['data']['movie']
    #     response['genres'] = ' '.join(response['genres'])
    #     yts_movies_details.append(response)
    #     counter = counter + 1
    #     print(counter)
    
    # columns = ['id', 'url', 'imdb_code', 'title', 'title_english', 'title_long', 'slug', 'year',
    #  'rating', 'runtime', 'genres', 'download_count', 'like_count', 'description_intro',
    #   'description_full', 'yt_trailer_code', 'language', 'mpa_rating', 'background_image',
    #  'background_image_original', 'small_cover_image', 'medium_cover_image', 'large_cover_image',
    #   'medium_screenshot_image1', 'medium_screenshot_image2', 'medium_screenshot_image3',
    #    'large_screenshot_image1', 'large_screenshot_image2', 'large_screenshot_image3', 'cast', 'torrents',
    #     'date_uploaded', 'date_uploaded_unix']

    write_to_csv(yts_movies_details, columns)

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, idx) for idx, url in enumerate(urls)]
        return await asyncio.gather(*tasks)

def yts_movie_details():
    prepare_urls()
    print("\n\nUrl preparation completed")
    asyncio.run(main())
    print("\n\nAPI Calling completed")
    write_to_csv(yts_movies_details, columns)
    print("\n\nWriting to csv completed")
    
def write_to_csv(data, columns):
    csv_file = '../movies/yts_movies.csv'
    try:
        with open(csv_file, 'w', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            for movie in data:
                writer.writerow(movie)
    except Exception as e:
        print(e)

yts_movie_details()