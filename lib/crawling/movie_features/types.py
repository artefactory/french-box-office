from typing import List, Tuple
try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict



class MovieCollection(TypedDict):
    id: int
    name: str


class MovieGenre(TypedDict):
    id: int
    name: str


class ProdCompany(TypedDict):
    id: int
    name: str
    origin_country: str


class ProdCountry(TypedDict):
    iso_code: str
    name: str


class Language(TypedDict):
    iso_code: str
    name: str



class MovieMember(TypedDict):
    adult: bool # Is playing in adult movies ?
    gender: int # 2 for male
    tmdb_id: int
    name: str # Name of member
    tmdb_popularity: float # ?
    order: int # the lower the most important


MovieCast = List[MovieMember]


class MovieDetails(TypedDict):
    tmdb_id: int 
    adult: bool # Is adult movie
    belongs_to_collection:  MovieCollection # Collection it eventually belongs to
    budget: int # Budget involved
    genres: List[MovieGenre] # Genres associated
    imdb_id: str 
    original_language: str # Production language
    original_title: str #
    overview: str # Movie description
    tmdb_popularity: float # ?
    production_companies: List[ProdCompany]
    production_countries: List[ProdCountry]
    release_date: str # Not the French date
    revenue: int #
    runtime: int 
    languages: List[Language] # Languages available (not always exhaustive)
    status: str
    tagline: str
    title: str # Title in French
    tmdb_vote_count: int
    tmdb_vote_average: float


class MovieCard(MovieDetails):
    cast: MovieCast


def unmarshal_credits(credits: dict) -> MovieCast:
    '''
    Decompose a TMDb movie credits response into a properly
    structured movie cast

    Parameters
    ----------
    credits: dict
        the movie credits response

    Returns
    -------
    cast: MovieCast
        A list of actors
    '''
    return [
        {
            'adult': cast['adult'],
            'gender': cast['gender'],
            'tmdb_id': cast['id'],
            'name': cast['name'],
            'tmdb_popularity': cast['popularity'],
            'order': cast['order']
        }
    for cast in credits.cast ] if credits.cast else []


def unmarshal_details(details: dict) -> MovieDetails:
    '''
    Decompose a TMDb movie details response into a properly
    structured movie card

    Parameters
    ----------
    details: dict
        the movie details response

    Returns
    -------
    card: MovieDetails
        A movie card
    '''
    return {
        'tmdb_id': details.id,
        'adult': details.adult,
        'belongs_to_collection': unmarshal_collection(details.belongs_to_collection) \
            if details.belongs_to_collection \
            else {},
        'budget': details.budget,
        'genres': unmarshal_genres(details.genres) \
            if details.genres \
            else [],
        'imdb_id': details.imdb_id,
        'original_language': details.original_language,
        'original_title': details.original_title,
        'overview': details.overview,
        'tmdb_popularity': details.popularity,
        'production_companies': unmarshal_prodcompanies(details.production_companies) \
            if details.production_companies \
            else [],
        'production_countries': unmarshal_prodcountries(details.production_countries) \
            if details.production_countries \
            else [],
        'release_date': details.release_date,
        'revenue': details.revenue,
        'runtime': details.runtime, 
        'languages': unmarshal_languages(details.spoken_languages) \
            if details.spoken_languages \
            else [],
        'status': details.status,
        'tagline': details.tagline,
        'title': details.title,
        'tmdb_vote_count': details.vote_count,
        'tmdb_vote_average': details.vote_average,
        'poster_path': details.poster_path
    }


def unmarshal_prodcompanies(companies: List[dict]) -> List[ProdCompany]:
    '''
    Decompose a TMDb production companies array 
    response into a properly list of Production Companies objects

    Parameters
    ----------
    companies: List[dict]
        The list of prod companies as given by tmdb api

    Returns
    -------
    prod_companies_list: List[ProdCompany]
        A list of production companies
    '''
    return [
        {
            'id': company['id'],
            'name': company['name'],
            'origin_country': company['origin_country']
        }
    for company in companies ]

def unmarshal_prodcountries(countries: List[dict]) -> List[ProdCountry]:
    '''
    Decompose a TMDb production countries array 
    response into a properly list of Production Countries objects

    Parameters
    ----------
    countries: List[dict]
        The list of prod countries as given by tmdb api

    Returns
    -------
    prod_countries_list: List[ProdCountry]
        A list of production countries
    '''
    return [
        {
            'iso_code': country['iso_3166_1'],
            'name': country['name'],
        }
    for country in countries ]


def unmarshal_languages(languages: List[dict]) -> List[Language]:
    '''
    Decompose a TMDb spoken_languages array 
    response into a properly list of languages objects

    Parameters
    ----------
    languages: List[dict]
        The list of spoken_languages as given by tmdb api

    Returns
    -------
    languages: List[Language]
        A list of languages
    '''
    return [
        {
            'iso_code': language['iso_639_1'],
            'name': language['name']
        }
    for language in languages ]


def unmarshal_collection(collection: dict) -> MovieCollection:
    '''
    Decompose a TMDb collection object as given by the API
    into a properly structured collection object

    Parameters
    ----------
    collection: dict
        The collection as given by tmdb api

    Returns
    -------
    collection: MovieCollection
        A movie collection
    '''
    return {
        'id': collection['id'],
        'name': collection['name']
    }

def unmarshal_genres(genres: List[dict]) -> List[MovieGenre]:
    '''
    Decompose a TMDb genres array 
    response into a properly list of genres objects

    Parameters
    ----------
    genres: List[dict]
        The list of genres as given by tmdb api

    Returns
    -------
    genres: List[LangMovieGenreuage]
        A list of genres
    '''
    return [
        {
            'id': genre['id'],
            'name': genre['name']
        }
    for genre in genres ]