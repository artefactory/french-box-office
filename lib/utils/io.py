from loguru import logger
import json
from typing import Union, List
import pandas as pd


def read_from_json(path: str) -> Union[dict, list]:
    '''
    Read and cast a json into a python object
    
    Parameters
    ----------
    path: str
        Path to json file

    Returns
    -------
    data: Union[dict, list]
        Json casted as python object
    '''
    with open(path, 'r') as infile:
        data = json.load(infile)
    return data


def load_dataset(path: str) -> pd.DataFrame:
    logger.info(f"loading raw data {path}...")
    data = pd.read_csv(path)
    data.drop(['title'], axis = 1, inplace = True)
    return data
