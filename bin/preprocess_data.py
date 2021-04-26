import pandas as pd
from config import ROOT_DIRPATH, FEATURE_COLS_TO_KEEP
from lib.preprocessing.encode import (encode_movie_data,
                                      get_encoded_collections_df,
                                      get_encoded_actors_df,
                                      get_mean_popularity)
from lib.utils.io import read_movies_entrees, read_movies_features
import os


def main():
    """This script does the encoding of the features, for the training dataset.
    """
    df_boxoffice = read_movies_entrees(os.path.join(ROOT_DIRPATH, 'data', 'french-box-office-29nov2020.json'))
    df_features = read_movies_features(os.path.join(ROOT_DIRPATH, 'data', 'movie-features-29nov2020.json'))
    data = pd.merge(df_boxoffice, df_features, on='id')
    data = data.loc[(data['sales'] != 0) & (data['sales'].notna())]
    data_final_cal = encode_movie_data(data)
    
    # TODO: adapt the following functions to make them work with new data
    df_collection = get_encoded_collections_df(data_final_cal)
    cols = ['year', 'title', 'release_date', 'collection_name', 'sales', 'rolling_sales_collection']
    df_all = pd.merge(data_final_cal, df_collection[cols], how = 'left', 
                  on = ['year', 'title', 'release_date', 'collection_name', 'sales']).fillna(0)
    df_all = get_mean_popularity(df_all, 3)
    df_all = get_mean_popularity(df_all, 5)
    df_all = get_encoded_actors_df(df_all)
    df_all = df_all.reindex(columns=FEATURE_COLS_TO_KEEP)
    df_all = df_all.fillna(0)
    df_all.to_csv(os.path.join(ROOT_DIRPATH, 'data', "processed_dataset.csv"), index=None)


if __name__ == '__main__':
    main()