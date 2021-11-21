from logger import Logger
from tmdb import Tmdb
import argparse
from enum import Enum
import re


class MediaType(Enum):
    MOVIE_GENERAL = "MOVIE_GENERAL"
    TV_SHOW_GENERAL = "TV_SHOW_GENERAL"
    MOVIE_ANIME = "MOVIE_ANIME"
    TV_SHOW_ANIME = "TV_SHOW_ANIME"
    MUSIC_ALBUM = "MUSIC_ALBUM"
    MUSIC_SINGLE = "MUSIC_SINGLE"
    MUSIC_COMPILATION = "MUSIC_COMPILATION"
    MUSIC_SOUNDTRACK_ANIME = "MUSIC_SOUNDTRACK_ANIME"
    MUSIC_SOUNDTRACK_GAMES = "MUSIC_SOUNDTRACK_GAMES"
    MUSIC_SOUNDTRACK_MOVIES = "MUSIC_SOUNDTRACK_MOVIES"
    MUSIC_SOUNDTRACK_TV_SHOW = "MUSIC_SOUNDTRACK_TV_SHOW"


class FileType(Enum):
    MP3 = "mp3"
    MP4 = "mp4"
    MKV = "mkv"
    AVI = "avi"
    FLAC = "flac"
    WAV = "wav"


config = {
    MediaType.MOVIE_GENERAL: {
        "destination_path": "D:\\1-Videos\\Films\\",
        "accepted_file_types": [FileType.MP4, FileType.MKV, FileType.AVI]
    }
}


def get_year_from_title(title: str) -> str:
    return re.findall("[1-3][0-9]{3}", title)[0]


def get_name_from_title(title: str) -> str:
    if "." in title:
        words = title.split(".")
        for word in words:
            # Check if word has has only letters with regex
            if not re.findall("[a-zA-Z]+", word):
                index = words.index(word)
                words = words[0:index]
                break

        torrent_name = " ".join(words)

    return torrent_name


def guess_media_type(title: str) -> str:
    """Try to guess the relevant media type from the title to better filter results from tmdb

    :param title: Title of the torrent
    :type title: str
    :return: The media type
    :rtype: str
    """

    # TV Show usually have the season in the title
    if re.findall("[Ss][0-3]?[1-9]", title):
        return "tv"
    return "movie"


def get_season_number(title: str) -> str:
    results = re.search("[Ss]([0-3]?[1-9])", title)
    if results:
        return results.group(1)
    return None


def main():
    logger = Logger("Main")
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', '-n', required=False,
                        help='Name of the torrent file',
                        dest='torrent_name', default="black.mirror.2019.s05")

    parser.add_argument('--content-path', required=False,
                        help='Path of the content',
                        dest='content_path', default="C:\\Users\\Antoine\\Downloads\\Last.Night.in.Soho.2021.MULTi.1080p.AMZN.WEB-DL.DDP5.1.H264-TkHD")

    parser.add_argument('--root-path', required=False,
                        help='Root path (used if it is a single file)',
                        dest='root_path')

    args = parser.parse_args()

    original_name = args.torrent_name
    content_path = args.content_path


    media_type = guess_media_type(original_name)
    torrent_year = get_year_from_title(original_name)
    torrent_name = get_name_from_title(original_name)

    tmdb = Tmdb()
    final_result = None

    if media_type == "movie":
        results = tmdb.search_movies(torrent_name)
    elif media_type == "tv":
        results = tmdb.search_tv_shows(torrent_name)
    else:
        logger.error(f"Unknown media type: {media_type}")
        results = tmdb.search_multi(torrent_name)

    if len(results) == 0:
        logger.warning(f"No results found for {torrent_name}")
        return

    if len(results) > 1:
        logger.info(f"Too many results. Trying to filter them with release date (year: {torrent_year})")
        for result in results:
            year_of_release = None
            if "release_date" in result:
                if result["release_date"]:
                    year_of_release = result["release_date"][0:4]
            elif "first_air_date" in result:
                if result["first_air_date"]:
                    year_of_release = result["first_air_date"][0:4]
            if year_of_release == torrent_year:
                final_result = result
                break

    if not final_result:
        final_result = results[0]

    logger.info(f"Final result: {final_result}")

    if media_type == "movie":
        title = final_result["title"]
    elif media_type == "tv":
        title = final_result["name"]
    else:
        title = final_result["title"]

    logger.info(f"Found a {media_type} with name: {title}")

    # If this is a TV Show, we must get the season
    if media_type == "tv":
        season_number = get_season_number(original_name)
        logger.info(f"Season number: {season_number}")


if __name__ == '__main__':
    main()
    input()
