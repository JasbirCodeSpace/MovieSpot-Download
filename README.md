# Movie Spot
A django web-app to list movie details and recommend similar movies based on movie search 
[Live Web-App](https://moviespotapp.herokuapp.com)

## Features

- Data from IMDB, TMDB and YTS
- Torrent files download option
- Movie Recommendation

# Installation

- Clone the repository

```bash
git clone https://github.com/JasbirCodeSpace/Movie-Recommendation-WebApp.git
```

- Install Dependencies

```bash
cd Movie-Recommendation-WebApp
pip install -r requirements.txt
```


- Run django migrations

```bash
pyhton manage.py makemigrations
python manage.py migrate
```

- Run django server

```bash
python manage.py runserver
```

