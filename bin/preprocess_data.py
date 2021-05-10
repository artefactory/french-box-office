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