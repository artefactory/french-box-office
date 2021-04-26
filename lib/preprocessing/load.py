import pandas as pd
from lib.utils.io import read_from_json
from typing import List


def read_movies_entrees(path: str) -> pd.DataFrame:
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
    bo = read_movies_entrees_from_loaded_json(bo)
    return bo


def read_movies_features(path: str) -> pd.DataFrame:
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
    features = read_movies_features_from_loaded_json(features)
    return features


def read_movies_features_from_loaded_json(features: List[dict]) -> pd.DataFrame:
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
    features = [
        {
            "is_adult": item['adult'],
            "is_part_of_collection": not not item['belongs_to_collection'], # Currently simple bool, may be interesting to use a more complex feature later
            "budget": item['budget'],
            "genres": [ genre['name'] for genre in item['genres'] ], 
            "original_language": item['original_language'],
            # "title": item['title'], # Can be challenged but chose to use title (french one) instead of original_title (in original language) as to have one single language for this feature
            # "overview": item['overview'], # Not used yet. Blob of text
            # "production_companies": item['production_companies'], # Not used yet. List of dicts with company id, country and name. 
            "production_countries": [ country['iso_code'] for country in item['production_countries'] ],
            "languages": [ language['iso_code'] for language in item['languages'] ],
            # "tagline": item['tagline'], # Not used yet. Blob of text
            # "production_companies": [ prod_comp['name'] for prod_comp in item['production_companies'] ],
            "runtime": item['runtime'],
            # "cast": item['cast'], # Not used yet. List of dicts with actor gender, name, id...
            "id": int(item['id'])
        } for item in features
    ]
    return pd.DataFrame(features)


def read_movies_entrees_from_loaded_json(bo: List[dict]) -> pd.DataFrame:
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


def get_dataset_from_api_res(movie_card: dict) -> pd.DataFrame:
    movie_features = read_movies_features_from_loaded_json([movie_card])
    movie_entree = read_movies_entrees_from_loaded_json([movie_card])
    return pd.merge(movie_features, movie_entree, on='id')
