from tmdbv3api import TMDb, Movie, Search
from typing import Union
from lib.crawling.movie_features.types import MovieDetails, unmarshal_details, MovieCast, unmarshal_credits, MovieCard

class TMDbClient:

    def __init__(self):
        '''
        A custom client for The Movie Database API for French movies
        '''
        self.client = TMDb()
        self.client.language = 'fr-FR'
        self.movie_db = Movie()
        self.search = Search()

    def find_movie_id(self, movie: str) -> Union[int, None]:
        '''
        Looks for a particular movie in TMDb

        Parameters
        ----------
        movie: str
            a movie title

        Returns
        -------
        id: Union[int, None]
            the most relevant movie id if we found one, or None
        '''
        results = self.search.movies({'query': movie})
        if len(results) > 0:
            return results[0].id

    def get_movie_details(self, movie_id: int) -> MovieDetails:
        '''
        Get a movie main features

        Parameters
        ----------
        movie_id: int
            a movie id (the tmdb one)

        Returns
        -------
        details: MovieDetails
            A movie details
        '''
        details = self.movie_db.details(movie_id)
        details = unmarshal_details(details)
        return details

    def get_movie_cast(self, movie_id: int) -> MovieCast:
        '''
        Get a movie cast

        Parameters
        ----------
        movie_id: int
            a movie id (the tmdb one)

        Returns
        -------
        cast: MovieCast
            A movie cast
        '''
        credits = self.movie_db.credits(movie_id)
        cast = unmarshal_credits(credits)
        return cast

    def find_movie_features(self, movie: str) -> Union[None, MovieCard]:
        '''
        Find all relevant features (details and cast)
        given a movie title

        Parameters
        ----------
        movie: str
            a movie title

        Returns
        -------
        card: Union[None, MovieCard]
            A movie card. None if no movie was found
        '''
        movie_id = self.find_movie_id(movie)
        if movie_id:
            card = self.get_movie_details(movie_id)
            card['cast'] = self.get_movie_cast(movie_id)
            return card
        else:
            return None
        


if __name__ == "__main__":

    from pprint import pprint

    client = TMDbClient()
    details = client.find_movie_features("Joker")
    pprint(details)