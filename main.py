# -*- coding: utf-8 -*-
from wrappers.auth import get_spotify
from wrappers.spotify_playlist import get_all_playlists, create_playlist, cache_playlists, add_to_playlist
from wrappers.spotify_tracks import get_all_tracks_from_playlist, append_audio_features, sort_list_by_attribute, \
    AudioAttribute


def list_matching_playlists(find_target_playlist: callable):
    """This will print all the playlist variants that were created."""
    spotify = get_spotify()

    playlists = get_all_playlists(spotify)
    matching_playlists = []
    for playlist in playlists:
        print(f"Looking through the playlist: {playlist.name}", end="\r", flush=True)
        if not find_target_playlist(playlist.name):
            continue

        matching_playlists.append(playlist)
        print(f"- {playlist.name} ({playlist.external_urls['spotify']})")

    return matching_playlists


def main(find_target_playlist: callable, create_playlists: bool):
    spotify = get_spotify()

    playlists = get_all_playlists(spotify)

    cache_playlists(playlists=playlists)

    tracks = []

    target_playlist_name = ""
    for playlist in playlists:
        print(f"Looking through the playlist: {playlist.name}", end="\r", flush=True)
        if not find_target_playlist(playlist.name):
            continue
        target_playlist_name = playlist.name
        print(f"Found target playlist: {target_playlist_name}")

        tracks = get_all_tracks_from_playlist(spotify, playlist.id)
        break

    full_tracks = append_audio_features(spotify, tracks)
    for attr in [attr for attr in AudioAttribute]:
        sorted_playlist_name = attr.value
        for is_reverse in [True, False]:
            sorted_tracks = sort_list_by_attribute(tracks=full_tracks, attribute=attr, reverse=is_reverse)
            variant_name = f"{sorted_playlist_name}__{'DESC' if is_reverse else 'ASC'}"
            with open(f"playlist_{variant_name}.txt", mode="w", encoding="utf-8") as file:
                file.writelines([f"{s_track.title} - {s_track.artist.name}\n" for s_track in sorted_tracks])

            if not create_playlists:
                continue
            spotify_playlist_name = f"{target_playlist_name} - {variant_name.replace('_', ' ')}".replace("  ", " ")
            sorted_playlist, from_cache = create_playlist(
                spotify=spotify,
                name=spotify_playlist_name,
                description="Created automatically using Python. 🤓🐍 "
                            "-- https://github.com/brenordv/spotify-playlist-sorter")

            add_to_playlist(spotify=spotify, playlist_id=sorted_playlist.id,
                            tracks=sorted_tracks, update_playlist=from_cache)


if __name__ == '__main__':
    # Change the lambda below to something that will match the playlist you want. You can simply change the text.
    main(find_target_playlist=lambda x: "2022" in x,
         create_playlists=True)
