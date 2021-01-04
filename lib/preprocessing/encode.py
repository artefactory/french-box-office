import pandas as pd
from typing import Optional
from sklearn.preprocessing import MultiLabelBinarizer

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