# -*- coding: utf-8 -*-
from typing import List, Union
from tekore import Spotify
from tekore._model import SimplePlaylist, FullPlaylist

from utils.list_utils import split_in_chunks
from wrappers.spotify_tracks import FullTrack, extract_uri_from_tracks, get_all_tracks_from_playlist

_playlists: List[SimplePlaylist] = []


def get_all_playlists(spotify: Spotify) -> List[SimplePlaylist]:
    playlists: List[SimplePlaylist] = []
    paginated_playlist = spotify.followed_playlists()
    playlists.extend(paginated_playlist.items)
    while len(playlists) < paginated_playlist.total:
        paginated_playlist = spotify.followed_playlists(offset=len(playlists))
        playlists.extend(paginated_playlist.items)

    return playlists


def _get_playlist_from_cache(name: str) -> Union[FullPlaylist, None]:
    global _playlists
    filtered = [pl for pl in _playlists if pl.name == name]

    return None if len(filtered) == 0 else filtered[0]


def create_playlist(spotify: Spotify, name: str, description: str = "", is_public: bool = True) -> (FullPlaylist, bool):
    playlist = _get_playlist_from_cache(name=name)

    if playlist is not None:
        return playlist, True

    user = spotify.current_user()
    playlist = spotify.playlist_create(
        user_id=user.id,
        name=name,
        description=description,
        public=is_public
    )

    cache_playlists([playlist, ])

    return playlist, False


def add_to_playlist(spotify: Spotify, playlist_id: str, tracks: List[FullTrack], update_playlist: bool) -> None:
    max_uris_per_request = 100
    uris = extract_uri_from_tracks(tracks)
    data_set = split_in_chunks(uris, n=max_uris_per_request)

    current_tracks = get_all_tracks_from_playlist(spotify=spotify, playlist_id=playlist_id)
    current_tracks_uri = extract_uri_from_tracks(current_tracks)

    has_replaced = False
    for uri_chunk in data_set:
        unique_uri_chunk = [uri for uri in uri_chunk if uri not in current_tracks_uri]

        if len(unique_uri_chunk) == 0:
            print("Adding 0 songs to playlist.", end="\r", flush=True)
            continue

        print(f"Adding {len(unique_uri_chunk)} songs to playlist. "
              f"Duplicated songs found: {len(uri_chunk) - len(unique_uri_chunk)}...", end="\r", flush=True)

        if update_playlist and not has_replaced:
            spotify.playlist_replace(playlist_id=playlist_id, uris=unique_uri_chunk)
            has_replaced = True

        spotify.playlist_add(playlist_id=playlist_id, uris=unique_uri_chunk)

        current_tracks_uri.extend(unique_uri_chunk)

    print(f"Added {len(current_tracks_uri)} songs to playlist!")


def cache_playlists(playlists: List[SimplePlaylist]) -> None:
    global _playlists
    _playlists.extend(playlists)
