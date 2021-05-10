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

from typing import Optional
from loguru import logger
import holidays
import numpy as np
import pandas as pd
from config import COUNTRY_TO_KEEP, DICT_GENRES, LANG_TO_KEEP, FEATURE_COLS_TO_KEEP
from sklearn.preprocessing import MultiLabelBinarizer
from vacances_scolaires_france import SchoolHolidayDates


def dummy_encode(
    data: pd.DataFrame, 
    column_to_encode: str,
    prefix: str,
    value_of_col_to_drop: Optional[str]=None) -> pd.DataFrame:
    '''
    Encodes one label variable `column_to_encode` from dataset `data`
    as multiple one hot encoding columns.

    Created columns will have `prefix_` as name prefix.

    As to handle multicolinearity, this function automatically
    drops a random column created, unless you provide a custom
    `value_of_col_to_drop` column name.

    E.g:
        data

            ```
                      original_language
            1                        fr
            2                        en
            3                        en
            4                        es
            ```
        
        dummy_encode(
            data, 
            'original_language',
            'original_language_is',
            'es'
        )

            ```
                original_language_is_fr  original_language_is_en
            1                         1                        0   
            2                         0                        1   
            3                         0                        1   
            4                         0                        0   
            ```
    

    Parameters
    ----------
    data: pd.DataFrame
        The initial dataset
    column_to_encode: str
        Name of column we should encode
    prefix: str
        Prefix we should use for new columns
    value_of_col_to_drop: Optional[str], default None
        Column created that needs to be dropped to avoid multicolinearity

    Returns
    -------
    df: pd.DataFrame
        The initial dataframe with the new one hot encoded features
    '''
    column_values = list(set(data[column_to_encode].to_list()))
    dummies = pd.get_dummies(data[column_to_encode], prefix=prefix)
    data = data.drop(column_to_encode, axis=1)
    data = data.join(dummies)
    if value_of_col_to_drop:
        data = data.drop(prefix+'_'+value_of_col_to_drop, axis=1)
    else:
        data = data.drop(prefix+'_'+column_values[0], axis=1)
    return data


def multilabel_encode(
    data: pd.DataFrame, 
    column_to_encode: str,
    prefix: Optional[str]=None,
    column_to_drop: Optional[str]=None) -> pd.DataFrame:
    '''
    Encodes one multilabel variable `column_to_encode` from dataset `data`
    as multiple one hot encoding columns.

    Columns to be encoded must be a pd.Series of with list values.

    You can provide a `prefix` for columns names.

    As to handle multicolinearity, this function automatically
    drops the first column created, unless you provide a custom
    `column_to_drop` column name.

    E.g:
        data

            ```
                                 genres
            1         [Action, Romance]
            2                [Thriller]
            3       [Thriller, Romance]
            4                  [Action]
            ```
        
        multilabel_encode(
            data, 
            'genres',
            None,
            'Action'
        )

            ```
                               Thriller                  Romance
            1                         0                        1   
            2                         1                        0   
            3                         1                        1   
            4                         0                        0   
            ```  

    Parameters
    ----------
    data: pd.DataFrame
        The initial dataset
    column_to_encode: str
        Name of column we should encode
    prefix: Optional[str], default None
        Prefix we should use for new columns
    column_to_drop: Optional[str], default None
        Column created that needs to be dropped to avoid multicolinearity

    Returns
    -------
    df: pd.DataFrame
        The initial dataframe with the new multilabels one hot encoded features
    '''
    mlb = MultiLabelBinarizer()
    data = data.join(
        pd.DataFrame(
            mlb.fit_transform(data.pop(column_to_encode)),
            columns=[ prefix+'_'+col for col in mlb.classes_ ] if prefix else mlb.classes_,
            index=data.index)
    )
    data = data.drop(column_to_drop if column_to_drop else mlb.classes_[0], axis=1)
    return data


def encode_movie_data(
        movie_data: pd.DataFrame, budget_median: Optional[float] = None, runtime_mean: Optional[float] = None, drop_cols: bool = True) -> pd.DataFrame:
    """This function aims to do the basic feature engineering and encoding for Movie data

    Args:
        movie_data (pd.DataFrame): sales and movie dataset merged
        budget_median (Optional[float], optional): If provided, will fill missing values, else will compute. Defaults to None.
        runtime_mean (Optional[float], optional): If provided, will fill missing values, else will compute. Defaults to None.
        drop_cols (bool): If True, will reindex dataset using FEATURE_COLS_TO_KEEP

    Returns:
        pd.DataFrame: dataframe with feature engineering and encoding
    """
    data = movie_data.copy()
    if budget_median is None:
        budget_median = np.median(data.loc[data['budget'] != 0]['budget'])
        logger.info(f'budget median: {budget_median}')
    data = fill_null_and_zero_values(data, 'budget', budget_median)
    if runtime_mean is None:
        runtime_mean = np.mean(data.loc[(data['runtime'] != 0) & (data['runtime'].isnull() == False)]['runtime'])
        logger.info(f'runtime_mean: {runtime_mean}')
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
    if drop_cols:
        data_final_cal = data_final_cal.reindex(columns=FEATURE_COLS_TO_KEEP)
    data_final_cal = data_final_cal.fillna(0)
    return data_final_cal


def reduce_lang_categories(lang_list, lang_to_keep=LANG_TO_KEEP):
    return list(set([el if el in lang_to_keep else 'other' for el in lang_list]))


def reduce_country_categories(country_list, country_to_keep=COUNTRY_TO_KEEP):
    return list(set([el if el in country_to_keep else 'OTHER' for el in country_list]))


def reduce_genre_categories(genre_list, dict_genres=DICT_GENRES):
    return list(set([dict_genres[el] for el in genre_list]))


def fill_null_and_zero_values(data, col_name, value):
    data.loc[(data[col_name] == 0) | (data[col_name].isnull()), col_name] = value
    return data


def fill_null_and_zero_values_for_countries(data):
    # For all movies where the production country is empty and the original language is french, we suppose that the
    # production country is France
    data.loc[(data.astype(str)['production_countries'] == '[]') & (
        data['original_language'] == 'fr'), 'production_countries'] = ['FR']

    # For all movies where the production country is empty and the original language is english, we suppose that the
    # production country is USA
    data.loc[(data.astype(str)['production_countries'] == '[]') & (
        data['original_language'] == 'en'), 'production_countries'] = ['US']

    # Elsewhere we put 'Other'
    data.loc[(data.astype(str)['production_countries'] == '[]'), 'production_countries'] = ['OTHER']
    return data


def encode_bool_to_numerical(data, col_name):
    dict_collection = {
        True: 1,
        False: 0
    }
    data[col_name] = data[col_name].map(dict_collection)
    return data


def get_encoded_languages_df(data_final):
    # Languages
    mlb = MultiLabelBinarizer()
    # Create a new dataset 'df_lang' that will contain one binary column for each language
    # (ex: available_lang_fr takes 1 if 'fr' was in the column 'languages', else 0)
    df_lang = pd.DataFrame(mlb.fit_transform(data_final['languages']), columns=mlb.classes_, index=data_final.index)
    df_lang.columns = ['available_lang_' + col for col in df_lang.columns]
    return df_lang


def get_encoded_genre_df(data_final):
    # Genres
    mlb = MultiLabelBinarizer()
    df_genre = pd.DataFrame(mlb.fit_transform(data_final['genres']), columns=mlb.classes_, index=data_final.index)
    return df_genre


def get_encoded_country_df(data_final):
    # Production countries
    mlb = MultiLabelBinarizer()
    df_country = pd.DataFrame(mlb.fit_transform(data_final['production_countries']), columns=mlb.classes_,
                            index=data_final.index)
    df_country.columns = ['prod_' + col for col in df_country.columns]
    return df_country


def get_encoded_calendar_df(data_final):
    # Load school holidays for France
    fr_holidays = SchoolHolidayDates()
    df_vacances = pd.DataFrame()
    for year in list(set(data_final['year'])):
        df_vacances = pd.concat([df_vacances, pd.DataFrame.from_dict(fr_holidays.holidays_for_year(year)).T])

    # Load bank holidays for France
    df_jf = pd.DataFrame()
    for year in list(set(data_final['year'])):
        df_jf = pd.concat([df_jf, pd.DataFrame([
            {'date': el[0], 'jour_ferie': el[1]} for el in sorted(holidays.FRA(years=year).items())])])
        
    # Merge school and bank holidays
    df_holidays = pd.merge(df_vacances, df_jf, how='outer', on='date')
    # Create features from df_holidays dataframes (school holidays and bank holidays):
    # - 3 binary features for school holidays, taking 1 if the given zone is on holiday, else 0 (vacances_zone_a, 
    # vacances_zone_b, vacances_zone_c)

    # Definition of a dictionary to encode boolean into numeric
    dict_map_vac = {
        True: 1,
        False: 0
    }
    # Apply dictionary to each holiday column for the three zones (A, B, C)
    df_holidays['vacances_zone_a'] = df_holidays['vacances_zone_a'].map(dict_map_vac)
    df_holidays['vacances_zone_b'] = df_holidays['vacances_zone_b'].map(dict_map_vac)
    df_holidays['vacances_zone_c'] = df_holidays['vacances_zone_c'].map(dict_map_vac)

    # - 1 binary feature for bank holiday, taking 1 if it is a bank holiday, else 0
    # The column "jour ferie" contains either the name of the holiday or a missing value (NaN)
    # The idea is to put a '1' when it's a holiday (i.e. when the value is different from nan, else 0)
    df_holidays['jour_ferie'] = df_holidays['jour_ferie'].map(lambda x: 1 if str(x) != 'nan' else 0)

    # - To go further: Try to create a combined feature with school and bank holidays
    df_holidays['holiday'] = df_holidays['vacances_zone_a'] + df_holidays['vacances_zone_b'] + df_holidays[
        'vacances_zone_c'] + df_holidays['jour_ferie']
    df_holidays['date'] = df_holidays['date'].map(lambda x: str(x))
    data_final_cal = pd.merge(data_final, df_holidays, how='left', left_on='release_date', right_on='date').fillna(0)
    data_final_cal['month'] = data_final_cal['release_date'].map(lambda x: int(x[5:7]))
    data_final_cal = apply_cos(data_final_cal, 'month', 'cos_month', 12)
    return data_final_cal


def apply_cos(df: pd.DataFrame,
              x: str, col_name: str, period: int) -> pd.DataFrame:
    """ Cos function on a column, for a specified period
    """
    df[col_name] = 2 * np.cos(2 * np.pi * df[x] / period)
    return df    


def get_encoded_collections_df(data_final_cal):

    # Collection with an high number of movies are often sagas that have worked well (ex: Star Wars, Fast and
    # Furious, ...)
    # We can therefore use the variable "is_part_of_collection" to compute the number of movies per collection
    # Hint: to create this kind of feature, you can use the .value_counts() method

    # Exclude collections with only one movie

    # We count the number of movies per collection
    df_count_col = data_final_cal.groupby(['collection_name']).count().reset_index()
    # We define a list of collection names with less than 2 movies (we won't take them into account)
    not_collection = list(set(df_count_col.loc[df_count_col['year'] < 2]['collection_name']))
    # For movies with less than 2 movies per collection, we set the values of "is_part_of_colleciton" to 0
    data_final_cal.loc[data_final_cal['collection_name'].isin(not_collection), 'is_part_of_collection'] = 0
    # For movies with less than 2 movies per collection, we set the values of "collection_name" to None
    data_final_cal.loc[data_final_cal['collection_name'].isin(not_collection), 'collection_name'] = None

    # Create the feature: number of movies per collection
    # We define a dictionary with the number of movies per collection (only collections with at least 2 movies since
    # we excluded the other ones just before)
    map_col_count = dict(data_final_cal['collection_name'].value_counts())
    # We remove the "None" collection (i.e. the first item of the dictionary that corresponds to all movies that are
    # not part of a collection)
    if len(map_col_count) > 0:
        del map_col_count[0]
        # We map the dictionary into a new feature: the number of movies per collection
        data_final_cal['nb_movie_collection'] = data_final_cal['collection_name'].map(map_col_count)
    else:
        data_final_cal['nb_movie_collection'] = 0

    # We isolate the movies that are part of a collection and we store it into df_collection
    df_collection = data_final_cal.loc[data_final_cal['is_part_of_collection'] == 1]
    # We compute the rolling average of the sales of the 10 previous movies per collection 
    df_collection['rolling_sales_collection'] = df_collection.sort_values(by=['collection_name', 'release_date']) \
                .groupby('collection_name')['sales'] \
                .transform(lambda x: x.rolling(10, 1).mean().shift())
    return df_collection


def get_encoded_actors_df(df_all):
    # To go (much much) further:
    # In the same vein, we could create features taking into account sales of previous movies per actor and create 
    # features that represent:
    # - for one movie, the mean of sales of previous movies of the #1 actor
    # - for one movie, the mean of sales of previous movies of the #2 actor
    # - for one movie, the mean of sales of previous movies of the #3 actor
    # - for one movie, the mean or the maximum of the three features above
    # This would also give an idea of an actor's "popularity"

    # /!\ For more details, this process is presented in the main deck, at the end of the feature engineering part 

    # We create three new columns with the names of the top 3 actors for each movie
    df_all['actor_1'] = df_all['cast'].map(lambda x: x[0]['name'] if len(x) > 0 else None) # name of actor #1
    df_all['actor_2'] = df_all['cast'].map(lambda x: x[1]['name'] if len(x) > 1 else None) # name of actor #2
    df_all['actor_3'] = df_all['cast'].map(lambda x: x[2]['name'] if len(x) > 2 else None) # name of actor #3
    # We define a list of all actors that appear in either #1, #2 or #3 positions for all movies
    actors_list = set(list(set(df_all['actor_1'])) + list(set(df_all['actor_2'])) + list(set(df_all['actor_3'])))

    k = 5
    df_all = df_all.sort_values('release_date')
    # For each actor we will compute the average of sales of its previous movies and we will copy this value to our
    # main dataframe when the given actor is in #1 or #2 or #3 position.
    for actor in list(actors_list):
        # We find all the movies where a given actor is in either #1, #2 or #3 position
        data_actor = df_all.loc[(df_all['actor_1'] == actor) | (df_all['actor_2'] == actor) | (df_all['actor_3'] == actor)]
        data_actor['actor'] = actor
        # We compute the average sales on its k previous movies (here k = 5)
        data_actor['mean_sales'] = data_actor.groupby('actor')['sales'] \
            .transform(lambda x: x.rolling(k, 1).mean().shift()).fillna(0)
        # We copy those values in the right place in our main dataframe
        df_all.loc[df_all['actor_1'] == actor, 'actor_1'] = data_actor.loc[data_actor['actor_1'] == actor, 'mean_sales']
        df_all.loc[df_all['actor_2'] == actor, 'actor_2'] = data_actor.loc[data_actor['actor_2'] == actor, 'mean_sales']
        df_all.loc[df_all['actor_3'] == actor, 'actor_3'] = data_actor.loc[data_actor['actor_3'] == actor, 'mean_sales']

    # We rename the columns to make them more understandable
    df_all = df_all.rename({
        'actor_1': 'actor_1_sales',
        'actor_2': 'actor_2_sales',
        'actor_3': 'actor_3_sales'
    }, axis=1)

    # We create two new features based on the ones created just above: the mean of the sales of the 3 main actors
    df_all['mean_sales_actor'] = (df_all['actor_1_sales'] + df_all['actor_2_sales'] + df_all['actor_3_sales']) / 3
    # and the maximum of the sales among the three main actors
    df_all['max_sales_actor'] = df_all[["actor_1_sales", "actor_2_sales", "actor_3_sales"]].max(axis=1)    
    return df_all    


def get_mean_popularity(df_all, top_n: int):
    df_all[f'mean_{top_n}_popularity'] = df_all['cast'].map(
        lambda x: np.mean([np.log(el['tmdb_popularity']) if np.log(el['tmdb_popularity']) > 0 else 0 for el in x[:top_n]])) \
            .fillna(0)
    return df_all    
