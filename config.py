import os
from lib.utils.path import get_project_root

# Paths
ROOT_DIRPATH = get_project_root()
TRAINING_DATASET_FILEPATH = os.path.join(ROOT_DIRPATH, "data", "data_prepared_session4.csv")

# Training 
BEST_K_FEATURES = 36                                          # K best features sorted by feature importance
LGBM_BEST_PARAMS = {'max_depth': 70, 'n_estimators': 80, 'num_leaves': 31}     # LightGBM hyperparameters
# Features sorted by importance:
FEATURE_IMPORTANCE = [
    'runtime',
    'mean_5_popularity',
    'mean_3_popularity',
    'budget',
    'actor_1_sales',
    'mean_sales_actor',
    'max_sales_actor',
    'actor_3_sales',
    'actor_2_sales',
    'month',
    'cos_month',
    'Comédie',
    'Drame',
    'is_part_of_collection',
    'rolling_sales_collection',
    'prod_FR',
    'Action',
    'prod_OTHER',
    'available_lang_fr',
    'original_lang_fr',
    'holiday',
    'Romance',
    'original_lang_en',
    'prod_US',
    'Familial',
    'nb_movie_collection',
    'Horreur',
    'available_lang_other',
    'prod_GB',
    'Other',
    'original_lang_other',
    'available_lang_it',
    'Fantastique',
    'available_lang_en',
    'vacances_zone_c',
    'vacances_zone_a',
    'available_lang_es',
    'vacances_zone_b',
    'prod_BE',
    'available_lang_de',
    'original_lang_ja',
    'prod_CA',
    'original_lang_it',
    'prod_DE',
    'available_lang_ja',
    'jour_ferie',
    'original_lang_es']