import pandas as pd
from config import TRAINING_DATASET_FILEPATH, ROOT_DIRPATH
from lib.preprocessing.encode import encode_movie_data
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
    data_final_cal.to_csv(TRAINING_DATASET_FILEPATH, index=None)


if __name__ == '__main__':
    main()