import os
import tmdbsimple as tmdb
from logger import Logger
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")


class Tmdb():
    def __init__(self) -> None:
        self.tmdb = tmdb
        self.tmdb.API_KEY = TMDB_API_KEY
        self.tmdb.REQUESTS_TIMEOUT = 5

        self.logger = Logger("TMDB")

    def search_multi(self, title: str) -> list:
        self.logger.info(f"Searching for {title}")
        response = self.tmdb.Search().multi(query=title)
        return response["results"]

    def search_movies(self, title: str) -> list:
        self.logger.info(f"Searching for movies with title: {title}")
        response = self.tmdb.Search().movie(query=title)
        return response["results"]

    def search_tv_shows(self, title: str) -> list:
        self.logger.info(f"Searching for TV shows with title: {title}")
        response = self.tmdb.Search().tv(query=title)
        return response["results"]

    def get_tv_show_by_id(self, id: int) -> dict:
        self.logger.info(f"Getting TV show with id: {id}")
        response = self.tmdb.TV(id).info()
        return response
