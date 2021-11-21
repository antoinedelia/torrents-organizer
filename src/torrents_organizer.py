from logger import Logger
from tmdb import Tmdb
import argparse
from enum import Enum


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


def main():
    logger = Logger("Main")
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', '-n', required=False,
                        help='Name of the torrent file',
                        dest='torrent_name', default="Last.Night.in.Soho.2021.MULTi.1080p.AMZN.WEB-DL.DDP5.1.H264-TkHD")

    parser.add_argument('--content-path', required=False,
                        help='Path of the content',
                        dest='content_path', default="C:\\Users\\Antoine\\Downloads\\Last.Night.in.Soho.2021.MULTi.1080p.AMZN.WEB-DL.DDP5.1.H264-TkHD")

    parser.add_argument('--root-path', required=False,
                        help='Root path (used if it is a single file)',
                        dest='root_path')

    args = parser.parse_args()

    torrent_name = args.torrent_name
    content_path = args.content_path

    tmdb = Tmdb()
    results = tmdb.search(torrent_name)
    logger.info(results)


if __name__ == '__main__':
    main()
    input()
