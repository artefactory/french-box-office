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

import pandas as pd
import numpy as np
from loguru import logger


def clean_data(data, drop_2020=True):
    logger.info("cleaning data..")
    data = data.dropna()
    if drop_2020:
        data = data.query("year != 2020")
    data = data.sort_values(by='release_date')
    data.release_date = pd.to_datetime(data.release_date)
    data.index = data.release_date
    data = data.drop(columns=['index', 'release_date', 'year'], errors='ignore')
    return data


def train_test_split_by_date(df: pd.DataFrame, split_date_val: str, split_date_test: str):
    """Split dataset according to a split date in format "YYYY-MM-DD"
    - train: [:split_date_1[
    - validation: [split_date_1: split_date_2[
    - test: [split_date_2:[
    """
    train = df.loc[:split_date_val].copy()
    validation = df.loc[split_date_val:split_date_test].copy()
    test = df.loc[split_date_test:].copy()
    return train, validation, test


def get_x_y(dataset):
    target = dataset.sales
    target = target.astype(float)
    features = dataset.drop(columns = ['sales'], errors='ignore')
    return features, target


def transform_target(target, forward = True):
    if forward == True: target_tf = [np.log(x) for x in target]
    else: target_tf = [np.exp(x) for x in target]
    return target_tf
