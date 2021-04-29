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

import argparse
import json
import time
from typing import Union
from tqdm import tqdm
from lib.crawling.movie_features.tmdb.client import TMDbClient
import os.path


def read_from_json(path: str) -> Union[list, dict]:
    with open(path, 'r') as infile:
        data = json.load(infile)
    return data

def save_json_file(payload: Union[list, dict], path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Extract relevant movie features from TMDb API based on a list of movie titles')
    parser.add_argument("-t", "--titles", type=str, required=True,
        help='A path to a json with movie titles and custom ids [{"id": "2ff8d8f6-bc8d-4b9e-a415-e0d4f87f0c53", "title": "Mission: Impossible 2"}]')
    parser.add_argument("-o", "--output", type=str, required=True,
        help='A path where you would like the results to be saved. In case the file already exists, the script will try to parse it and only send a request for movies not already crawled.')

    args = parser.parse_args()
    tmdb_client = TMDbClient()

    # Read requested scope
    scope = read_from_json(args.titles)
    
    # See if we already have some data
    if os.path.isfile(args.output):
        results = read_from_json(args.output)
        existing_ids = set([ movie['id'] for movie in results ])
    else:
        results = []
        existing_ids = set()

    # For all movies listed send a request
    for i, movie in enumerate(tqdm(scope)):

        movie_id = movie['id']
        if movie_id not in existing_ids:
            movie_card = tmdb_client.find_movie_features(movie['title'])

            # If response is not null, write to results
            if movie_card:
                movie_card['id'] = movie_id
                movie_card['query'] = movie['title']

                results.append(movie_card)

            # Give some rest to TMDB
            time.sleep(0.1)
        
        if i != 0 and i % 1000 == 0:
            save_json_file(results, args.output)
        


    
    # Finally write results to disk
    save_json_file(results, args.output)
