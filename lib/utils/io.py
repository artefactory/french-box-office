# Copyright (C) 2020 Artefact
# licence-information@artefact.com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from lib.crawling.movie_features.tmdb.client import TMDbClient
from loguru import logger
import json
import pandas as pd


def read_from_json(path):
    '''
    Read and cast a json into a python object
    
    Parameters
    ----------
    path: str
        Path to json file

    Returns
    -------
    data: Union[dict, list]
        Json casted as python object
    '''
    data = json.load(open(path, 'r', encoding='utf-8', errors="ignore"))
    return data


def load_dataset(path: str) -> pd.DataFrame:
    logger.info(f"loading raw data {path}...")
    data = pd.read_csv(path)
    return data


def read_movies_entrees(path):
    '''
    Read the box office dataset 
    and casts it as an usable pandas DataFrame

    Parameters
    ----------
    path: str
        path to the dataset

    Returns
    -------
    df: pd.DataFrame
        Data as DataFrame
    '''
    bo = read_from_json(path)
    bo = [
        {
            "year": item['year'], 
            "title": item['title'], 
            "id": int(item['id']), 
            "sales": item['first_week_sales'],
            "release_date": item['release_date']
        } for item in bo
    ]
    return pd.DataFrame(bo)


def read_movies_features(path):
    '''
    Read the movie features dataset 
    and casts it as an usable pandas DataFrame
    N.B: Fields that are not yet used are commented
    Parameters
    ----------
    path: str
        path to the dataset
    Returns
    -------
    df: pd.DataFrame
        Data as DataFrame
    '''
    features = read_from_json(path)
    features = [
        {
            "is_adult": item['adult'],
            "is_part_of_collection": not not item['belongs_to_collection'],
            "collection_name": item['belongs_to_collection']['name'] if item['belongs_to_collection'] != {} else None, # Currently simple bool, may be interesting to use a more complex feature later
            "budget": item['budget'],
            "genres": [ genre['name'] for genre in item['genres'] ], 
            "original_language": item['original_language'],
            "overview": item['overview'], # Not used yet. Blob of text
            "production_countries": [ country['iso_code'] for country in item['production_countries'] ],
            "languages": [ language['iso_code'] for language in item['languages'] ],
            "tagline": item['tagline'], # Not used yet. Blob of text
            "runtime": item['runtime'],
            "cast": item['cast'], # Not used yet. List of dicts with actor gender, name, id...
            "id": int(item['id'])
        } for item in features
    ]
    return pd.DataFrame(features)
