import numpy as np
import pandas as pd
from config import LANG_TO_KEEP, ROOT_DIRPATH
from lib.preprocessing.encode import (fill_null_and_zero_values,
                                      fill_null_and_zero_values_for_countries,
                                      reduce_country_categories,
                                      reduce_genre_categories,
                                      reduce_lang_categories,
                                      encode_bool_to_numerical,
                                      get_encoded_languages_df, 
                                      get_encoded_genre_df,
                                      get_encoded_country_df,
                                      get_encoded_calendar_df,
                                      get_encoded_collections_df,
                                      get_encoded_actors_df,
                                      get_mean_popularity)
from lib.utils.io import read_movies_entrees, read_movies_features
import os


def main():
    df_boxoffice = read_movies_entrees(os.path.join(ROOT_DIRPATH, 'data', 'french-box-office-29nov2020.json'))
    df_features = read_movies_features(os.path.join(ROOT_DIRPATH, 'data', 'movie-features-29nov2020.json'))
    data = pd.merge(df_boxoffice, df_features, on='id')
    data = data.loc[(data['sales'] != 0) & (data['sales'].notna())]
    budget_median = np.median(data.loc[data['budget'] != 0]['budget'])
    #data = fill_null_and_zero_values(data, 'sales', budget_median)
    runtime_mean = np.mean(data.loc[(data['runtime'] != 0) & (data['runtime'].isnull() == False)]['runtime'])
    data = fill_null_and_zero_values(data, 'runtime', runtime_mean)
    data = fill_null_and_zero_values_for_countries(data)
    data['original_language'] = data['original_language'].map(lambda x: x if x in LANG_TO_KEEP else 'other')
    data['languages'] = data['languages'].map(lambda x: reduce_lang_categories(x))
    data['production_countries'] = data['production_countries'].map(lambda x: reduce_country_categories(x))
    data['genres'] = data['genres'].map(lambda x: reduce_genre_categories(x))
    data = encode_bool_to_numerical(data, 'is_part_of_collection')
    data_final = pd.get_dummies(data, prefix='original_lang', columns=['original_language'], drop_first=True)
    data_final = data_final.set_index('id')
    df_lang = get_encoded_languages_df(data_final)
    df_genre = get_encoded_genre_df(data_final)
    df_country = get_encoded_country_df(data_final)
    data_final = pd.merge(data_final, df_lang, left_index=True, right_index=True) \
               .merge(df_genre, left_index=True, right_index=True) \
               .merge(df_country, left_index=True, right_index=True)
    data_final_cal = get_encoded_calendar_df(data_final)
    df_collection = get_encoded_collections_df(data_final_cal)
    cols = ['year', 'title', 'release_date', 'collection_name', 'sales', 'rolling_sales_collection']
    df_all = pd.merge(data_final_cal, df_collection[cols], how = 'left', 
                  on = ['year', 'title', 'release_date', 'collection_name', 'sales']).fillna(0)
    df_all = get_mean_popularity(df_all, 3)
    df_all = get_mean_popularity(df_all, 5)
    df_all = get_encoded_actors_df(df_all)
    to_drop = ['nom_vacances', 'date', 'genres', 'production_countries', 'languages', 'is_adult', 'collection_name',
           'overview', 'tagline', 'cast']
    df_all = df_all.drop(to_drop, axis=1).reset_index()
    df_all = df_all.fillna(0)
    df_all.to_csv(os.path.join(ROOT_DIRPATH, 'data', "processed_dataset.csv"), index=None)


if __name__ == '__main__':
    main()