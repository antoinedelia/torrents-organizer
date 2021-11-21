import os
import tmdbsimple as tmdb

TMDB_API_KEY = os.environ.get("TVDB_API_KEY")


class Tmdb():
    def __init__(self) -> None:
        self.tmdb = tmdb
        self.tmdb.API_KEY = TMDB_API_KEY
        self.tmdb.REQUESTS_TIMEOUT = 5

    def search(self, name: str) -> dict:
        results = self.tmdb.Search().multi(query=name)
        return results
