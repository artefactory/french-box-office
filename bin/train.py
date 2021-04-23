import os

import pandas as pd
from config import (BEST_K_FEATURES, FEATURE_IMPORTANCE, LGBM_BEST_PARAMS,
                    LGBM_MODEL_FILEPATH, TRAINING_DATASET_FILEPATH)
from lib.evaluation.evaluate import evaluate
from lib.modelling.training import save_model, train
from lib.preprocessing.preprocess import (clean_data, get_x_y,
                                          train_test_split_by_date,
                                          transform_target)
from lib.utils.io import load_dataset
from lightgbm import LGBMRegressor
from loguru import logger


def training_workflow():
    raw_data = load_dataset(TRAINING_DATASET_FILEPATH)
    data = clean_data(raw_data, drop_2020=False)
    train_data, validation_data, test_data = train_test_split_by_date(data,
                                                                    '2018-01-01',
                                                                    '2020-01-01')
    train_x, train_y = get_x_y(train_data)
    validation_x, validation_y = get_x_y(validation_data)
    test_x, test_y = get_x_y(test_data)
    lgbm = LGBMRegressor(**LGBM_BEST_PARAMS)
    features_list = FEATURE_IMPORTANCE[:BEST_K_FEATURES+1]
    msg = f"Training fitting LightGBM using features: {features_list}"
    msg += f"hyper-parameters: {LGBM_BEST_PARAMS}"
    logger.info(msg)
    lgbm = train(lgbm, train_x[features_list], train_y, transformer=transform_target)
    logger.info("Evaluate on validation set ...")
    evaluate(lgbm, validation_x[features_list], validation_y, transformer=transform_target)
    logger.info("Evaluate on test set...")
    evaluate(lgbm, test_x[features_list], test_y, transformer=transform_target)
    save_model(lgbm, LGBM_MODEL_FILEPATH)

if __name__ == '__main__':
    training_workflow()
