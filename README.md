# french-box-office

Predicting French movies success

## Install and Set up

Set-up once and for all a dedicated conda environment:

```bash
conda create -y -n french_box_office python=3.7
conda activate french_box_office
```

Install then the requirements and export the path:

```bash
pip install -r requirements.txt
export PYTHONPATH="."
```


## Usage

### Crawling movies sales

French box-office statistics are gently crawled from the website [jpbox-office](http://jpbox-office.com) using [`scrapy`](https://scrapy.org/). You can refresh this data by typing the following commands:

```bash
cd lib/crawling/boxoffice
scrapy crawl jpbox -a start_year=2000 -a end_year=2020 -o ../../../../data/french-box-office-23nov2020.json
```

It will create the following `json`:

```
[
    {
        "id": "17528", // Source website id
        "year": 2019, // Year of release
        "rank": "1", // Rank in sales during the year of release
        "title": "Le Roi Lion (2019)", // Movie title
        "total_sales": 10017995, // Sales (nombre d'entrées) since release
        "release_date": "2019-07-17", // Date of release in France
        "max_theaters_used": 820, // Maximum number of theaters where the movie was screened during a week
        "first_screening_sales": null, // Sales for the first screening (not always filled in)
        "first_day_sales": 630478, // Sales on the first day
        "first_weekend_sales": 2559370, // Sales on the first weekend
        "first_week_sales": 3252896 // Sales on the week
    },
    ...
]
```

### Getting movies features

Movie features are extracted via [The Movie Database API](https://developers.themoviedb.org/3/getting-started/introduction). Create an account on their website and export your API key:

```bash
export TMDB_API_KEY='your-key-here'
```

You can then directly provide the previous "sales" json to the following script to get movie features:

```bash
python bin/get_movie_features.py --titles data/french-box-office-23nov2020.json --output data/movie-features-24nov2020.json
```

The movie titles will be used as a query parameters to TMDb API. If we get a match, further details will be extracted from the API. A typical results will be like (original query and `id` are kept in the result):

```
[    
    {
        "tmdb_id": 2332,
        "adult": false,
        "belongs_to_collection": {
            "id": 211721,
            "name": "Taxi - Saga"
        },
        "budget": 0,
        "genres": [
            {
                "id": 28,
                "name": "Action"
            },
            {
                "id": 35,
                "name": "Comédie"
            }
        ],
        "imdb_id": "tt0183869",
        "original_language": "fr",
        "original_title": "Taxi 2",
        "overview": "Daniel, le chauffeur de taxi dingue de vitesse, et Emilien, l'inspecteur de police inexpérimenté, se retrouvent à Paris. Le ministre de la défense japonais vient tester le savoir-faire hexagonal en matière de lutte antiterroriste et signer le contrat du siècle avec l'Etat français. Mais il est enlevé par des yakusas...",
        "tmdb_popularity": 12.892,
        "production_companies": [
            {
                "id": 189,
                "name": "ARP Sélection",
                "origin_country": "FR"
            },
            {
                "id": 356,
                "name": "TF1 Films Production",
                "origin_country": "FR"
            },
            {
                "id": 104,
                "name": "Canal+",
                "origin_country": "FR"
            },
            {
                "id": 121921,
                "name": "Leeloo Productions",
                "origin_country": ""
            }
        ],
        "production_countries": [
            {
                "iso_code": "FR",
                "name": "France"
            }
        ],
        "release_date": "2000-03-24",
        "revenue": 60726164,
        "runtime": 88,
        "languages": [
            {
                "iso_code": "de",
                "name": "Deutsch"
            },
            {
                "iso_code": "fr",
                "name": "Français"
            },
            {
                "iso_code": "ja",
                "name": "日本語"
            }
        ],
        "status": "Released",
        "tagline": "Attachez vos ceintures, il passe la seconde !",
        "title": "Taxi 2",
        "tmdb_vote_count": 1113,
        "tmdb_vote_average": 6.2,
        "cast": [
            {
                "adult": false,
                "gender": 2,
                "tmdb_id": 20666,
                "name": "Samy Naceri",
                "tmdb_popularity": 6.409,
                "order": 0
            },
            {
                "adult": false,
                "gender": 2,
                "tmdb_id": 23943,
                "name": "Frédéric Diefenthal",
                "tmdb_popularity": 1.4,
                "order": 1
            },
            {
                "adult": false,
                "gender": 1,
                "tmdb_id": 8293,
                "name": "Marion Cotillard",
                "tmdb_popularity": 18.542,
                "order": 2
            },
            {
                "adult": false,
                "gender": 1,
                "tmdb_id": 23944,
                "name": "Emma Wiklund",
                "tmdb_popularity": 3.811,
                "order": 3
            },
            ...
        ],
        "id": "2398",
        "query": "Taxi 2"
    },
    ...
]
```
