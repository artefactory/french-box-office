from lib.workflows.inference import infer_from_movie_title
from pprint import pprint

MOVIE_TITLE = "Kaamelott : Premier volet"


if __name__ == "__main__":
    movie_card = infer_from_movie_title(MOVIE_TITLE)
    pprint(movie_card)