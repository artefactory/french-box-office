import dotenv
import lightgbm as lgb
from config import BUDGET_MEDIAN, LGBM_MODEL_FILEPATH, RUNTIME_MEAN
from lib.crawling.movie_features.tmdb.client import (
    TMDbClient, query_movie_data_from_title)
from lib.modelling.predict import predict
from lib.preprocessing.encode import encode_movie_data
from lib.preprocessing.load import get_dataset_from_api_res
from lib.preprocessing.preprocess import clean_data, get_x_y, transform_target
from loguru import logger


def infer_from_movie_title(title: str) -> dict:
    logger.info(f"Fetching prediction for {title}")
    dotenv.load_dotenv(dotenv.find_dotenv())
    tmdb_client = TMDbClient()
    movie_card, status = query_movie_data_from_title(tmdb_client, title)
    if status["success"]:
        movie_data = get_dataset_from_api_res(movie_card)
        movie_data = encode_movie_data(movie_data, budget_median=BUDGET_MEDIAN, runtime_mean=RUNTIME_MEAN)
        data_clean = clean_data(movie_data, drop_2020=False)
        X, _ = get_x_y(data_clean)
        model = lgb.Booster(model_file=LGBM_MODEL_FILEPATH)
        predictions = predict(model, X, transformer=transform_target)
        movie_card['box_office_sales_forecast'] = predictions[0]
        movie_card["success"] = True
        logger.success(f"Forecast result: {predictions[0]}")
        return movie_card
    else:
        return status
