from os import getenv
from logging import getLogger
from coloredlogs import install
from bisect import bisect
from math import ceil
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException
from utils.arg_parse import args, options, parser
from random import randint


class NoPlaylistNameProvided(Exception):
    pass

class NoTrackNameProvided(Exception):
    pass

class NoTracksFound(Exception):
    pass

class NoArtistNameProvided(Exception):
    pass

class NoArtistFound(Exception):
    pass


logger = getLogger(__name__)
install(
    fmt="\n%(asctime)s [%(hostname)s] [%(name)s] [%(levelname)8s] :\t%(message)s\n",
    level="DEBUG",
    logger=logger
)


class spotiCLI():
    def __init__(self):
        self.user_id = getenv("spotify_user_id")
        self.token = SpotifyOAuth(
            client_id=getenv("spotify_client_id"),
            client_secret=getenv("spotify_client_secret"),
            redirect_uri=getenv("spotify_redirect_uri"),
            scope=[
                "user-follow-read",
                "playlist-modify-private",
                "playlist-modify-public",
                "playlist-read-private",
                "playlist-read-collaborative",
                "user-read-currently-playing",
            ]
        )
        self.spotify = Spotify(auth_manager=self.token)
        self.start

    @property
    def start(self):
        to_do = {
            "c": self.create_playlist,
            "d": self.delete_playlist,
            "v": self.display_user_playlist,
            "t": self.track_info,
            "a": self.artist_info,
            "s": self.sort_playlist_acc_to_release_date,
            "i": self.add_track_to_playlist,
            "p": self.current_track,
        }
        true_char = [key[0] for key, value in options.__dict__.items() if value is True]
        if not true_char:
            return parser.print_help()
        action = to_do.get(true_char[0])
        action()

    def search(self, response, type, limit):
        return self.spotify.search(q=response, type=type, limit=limit)

    def get_playlist_name(self, playlist_id):
        return self.spotify.playlist(playlist_id)["name"]

    def get_playlist_length(self, playlist_id):
        return self.spotify.playlist(playlist_id)["tracks"]["total"]

    def get_all_data(self, obj):
        items = obj["items"]
        while obj["next"]:
            obj = self.spotify.next(obj)
            items.extend(obj["items"])
        return items
    
    def get_playlist_obj(self):
        return self.spotify.current_user_playlists()

    def get_playlist_items(self, playlist_id):
        return self.spotify.playlist_items(playlist_id)

    def get_playlist_id_from_no(self, playlist_no):
        return self.get_all_data(self.get_playlist_obj())[playlist_no-1]["id"]

    def get_playlist_id_list_from_no(self, p_numbers):
        p_numbers = tuple(map(int, p_numbers.split()))
        playlist_ids = []
        for i in p_numbers:
            playlist_ids.append(self.get_playlist_id_from_no(i))
        return playlist_ids
    
    def get_user_track_data(self, data, track_no, key):
        return data[track_no][key]

    def check_track_year_only(self, tracks):
        for _ in tracks:
            if _[4]!="-":
                tracks[tracks.index(_)] = "XXXXXX" + _
        return tracks

    def display_found_tracks(self, data, no_of_tracks):
        for _ in range(no_of_tracks):
            print(f'{str(_+1).zfill(2)}. {", ".join((i["name"] for i in data[_]["artists"]))} - {data[_]["name"]}')

    def get_position_index(self, position, track_release, playlist_id, playlist_length):
        if position==1:
            return position-1
        elif position==2:
            return playlist_length
        elif position==3:
            return randint(0, playlist_length)
        track_list = self.get_all_data(self.get_playlist_items(playlist_id))
        track_list = [track_list[_]["track"]["album"]["release_date"] for _ in range(playlist_length)]
        return bisect(track_list, track_release)

    def display_track_info(self, data):
        print("\n".join((
                f'\nTrack_name: {data["name"]}',
                f'Duration: {str(data["duration_ms"]//60000).zfill(2)}:{str((data["duration_ms"]//1000)%60).zfill(2)}',
                f'Contributing_artists: {", ".join((_["name"] for _ in data["artists"]))}',
                f'Album_name: {data["album"]["name"]}',
                f'Album_artists: {data["album"]["artists"][0]["name"]}',
                f'Album_type: {data["album"]["album_type"].title()}',
                f'Album_release_date: {data["album"]["release_date"]}'
        )))

    def add_tracks(self, playlist_id, tracks):
        x = len(tracks)
        no_will_run = ceil(x/100)
        ind_inc = 0
        ind_rng = x if x<100 else 100

        for _ in range(no_will_run):
            trks = tracks[ind_inc:] if _+1 == no_will_run else tracks[ind_inc:ind_rng]
            self.spotify.playlist_add_items(playlist_id, trks)
            ind_inc += 100
            ind_rng += 100

    def create_playlist(self):
        try:
            if not args:
                raise NoPlaylistNameProvided
            for arg in args:
                self.spotify.user_playlist_create(
                    user=self.user_id,
                    name=arg
                )
                logger.info(f"Playist name {arg} created successfully!")

        except NoPlaylistNameProvided:
            logger.error("You must provide atleast one playlist name!")

    def delete_playlist(self):
        try:
            self.display_user_playlist()
            playlists = input("select playlist no.(s) to delete: ")
            playlist_ids = self.get_playlist_id_list_from_no(playlists)
            for i in playlist_ids:
                logger.info(f"Playlist name {self.get_playlist_name(i)} deleted successfully!")
                self.spotify.current_user_unfollow_playlist(i)

        except SpotifyException:
            logger.error("Playlist not found!")

    def display_user_playlist(self):
        obj = self.get_playlist_obj()
        playlists = self.get_all_data(obj)
        total_no_of_playlist = obj["total"]
        print(f"\nTotal no. of playlists: {total_no_of_playlist}\n")

        if(total_no_of_playlist==0):
            return 0
        for _ in range(total_no_of_playlist):
            print(f'{str(_+1).zfill(2)}. {playlists[_]["name"]}')
        return 1

    def track_info(self):
        try:
            if not args:
                raise NoTrackNameProvided
            obj = self.search(" ".join(args), "track", 1)
            
            if not obj["tracks"]["items"]:
                raise NoTracksFound
            data = obj["tracks"]["items"][0]

            self.display_track_info(data)

        except NoTrackNameProvided:
            logger.error("You must provide a track name!")
        
        except NoTracksFound:
            logger.error("No tracks found!")

    def artist_info(self):
        try:
            if not args:
                raise NoArtistNameProvided
            obj = self.search(" ".join(args), "artist", 1)

            if not obj["artists"]["items"]:
                raise NoArtistFound

            data = obj["artists"]["items"][0]

            print("\n".join((
                f'\nName: {data["name"]}',
                f'Followers: {data["followers"]["total"]}'
            )))

        except NoArtistNameProvided:
            logger.error("You must provide an artist name!")

        except NoArtistFound:
            logger.error("No artists found!")

    def sort_playlist_acc_to_release_date(self):
        
        self.display_user_playlist()
        playlists = input("select playlist no.(s) to sort: ")
        playlist_ids = self.get_playlist_id_list_from_no(playlists)

        for id in playlist_ids:
            obj = self.get_playlist_items(id)
            tracks = self.get_all_data(obj)
            
            no_of_tracks = self.get_playlist_length(id)
            sorted_tracks_id = [tracks[_]["track"]["album"]["release_date"]+tracks[_]["track"]["id"] for _ in range(no_of_tracks)]
            sorted_tracks_id.sort()

            sorted_tracks_id = self.check_track_year_only(sorted_tracks_id)
            sorted_tracks_id = [_[10:] for _ in sorted_tracks_id]

            self.spotify.playlist_replace_items(id, items=[])
            self.add_tracks(id, sorted_tracks_id)

            logger.info(f"Playlist name {self.get_playlist_name(id)} updated successfully!")

    def add_track_to_playlist(self):
        response = input("enter the name of the track: ")
        obj = self.search(response, "track", 10)
        data = obj["tracks"]["items"]
        no_of_tracks = len(data)
        print(f"\n{no_of_tracks} tracks found!:\n")
        
        if no_of_tracks==0:
            return

        self.display_found_tracks(data, no_of_tracks)
        response = int(input("select track no. to add to playlist: "))
        
        if(self.display_user_playlist()==0):
            return

        playlist_no = int(input("select playlist no. to add the track: "))
        playlist_id = self.get_playlist_id_from_no(playlist_no)
        track = self.get_user_track_data(data, response-1, "id")

        playlist_length = self.get_playlist_length(playlist_id)
        position = int(input("\n".join(("\n1. Top", "2. Bottom", "3. Random", "4. Date sorted", "\nSelect position to add track: "))))
        track_release = data[response-1]["album"]["release_date"]
        position = self.get_position_index(position, track_release, playlist_id, playlist_length)
        self.spotify.playlist_add_items(playlist_id, [track], position)

        logger.info(f'Track: {self.get_user_track_data(data, response-1, "name")} added to Playlist: {self.get_playlist_name(playlist_id)} at position: {position+1}')

    def current_track(self):
        try:
            data = self.spotify.current_user_playing_track()["item"]
            print("\nDisplaying current playing track: ", end="")
            self.display_track_info(data)

        except TypeError:
            logger.info("Not playing anything atm!")