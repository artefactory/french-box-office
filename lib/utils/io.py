import json
from typing import Union, List

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