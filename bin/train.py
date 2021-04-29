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

from config import (LGBM_BEST_PARAMS,
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
    """This script does the model training and saving
    """    
    raw_data = load_dataset(TRAINING_DATASET_FILEPATH)
    data = clean_data(raw_data, drop_2020=False)
    train_data, validation_data, test_data = train_test_split_by_date(data,
                                                                    '2018-01-01',
                                                                    '2020-01-01')
    train_x, train_y = get_x_y(train_data)
    validation_x, validation_y = get_x_y(validation_data)
    test_x, test_y = get_x_y(test_data)
    lgbm = LGBMRegressor(**LGBM_BEST_PARAMS)
    msg = f"Training LightGBM using hyper-parameters: {LGBM_BEST_PARAMS}"
    logger.info(msg)
    lgbm = train(lgbm, train_x, train_y, transformer=transform_target)
    logger.info("Evaluate on validation set ...")
    evaluate(lgbm, validation_x, validation_y, transformer=transform_target)
    logger.info("Evaluate on test set...")
    evaluate(lgbm, test_x, test_y, transformer=transform_target)
    save_model(lgbm, LGBM_MODEL_FILEPATH)

if __name__ == '__main__':
    training_workflow()
