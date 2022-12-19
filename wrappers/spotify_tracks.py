# -*- coding: utf-8 -*-
from enum import Enum
from functools import partial
from typing import List, Union
from tekore import Spotify
from tekore._model import AudioFeatures, FullPlaylistTrack, LocalPlaylistTrack, PlaylistTrackPaging, FullPlaylistEpisode

from utils.list_utils import split_in_chunks


class AudioAttribute(Enum):
    """Audio Features descriptions from here:
    https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features"""

    """A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence
    the track is acoustic.
    >= 0<= 1"""
    Acoustic = "acousticness"

    """Danceability describes how suitable a track is for dancing based on a combination of musical elements including
    tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is
    most danceable."""
    Danceability = "danceability"

    """The duration of the track in milliseconds."""
    Length = "duration_ms"

    """Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, 
    energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores 
    low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, 
    timbre, onset rate, and general entropy."""
    Energy = "energy"

    """Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. 
    Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater 
    likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, 
    but confidence is higher as the value approaches 1.0."""
    Instrumental = "instrumentalness"

    """The key the track is in. Integers map to pitches using standard Pitch Class notation. 
    E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.
    >= -1<= 11
    https://en.wikipedia.org/wiki/Pitch_class
    """
    Key = "key"

    """Detects the presence of an audience in the recording. Higher liveness values represent an increased probability 
    that the track was performed live. A value above 0.8 provides strong likelihood that the track is live."""
    Live = "liveness"

    """The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are 
    useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary 
    psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db."""
    Loudness = "loudness"

    """Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is 
    derived. Major is represented by 1 and minor is 0."""
    Mode = "mode"

    """Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording 
    (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks 
    that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain 
    both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most 
    likely represent music and other non-speech-like tracks."""
    Speechiness = "speechiness"

    """The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or 
    pace of a given piece and derives directly from the average beat duration."""
    BeatsPerMinute = "tempo"

    """An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are 
    in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4".
    >= 3<= 7"""
    TimeSignature = "time_signature"

    """A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound
     more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, 
     depressed, angry).
    >= 0<= 1"""
    Valence = "valence"

    """The popularity of the track. The value will be between 0 and 100, with 100 being the most popular.
    The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is 
    calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how 
    recent those plays are. Generally speaking, songs that are being played a lot now will have a higher popularity 
    than songs that were played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) 
    are rated independently. Artist and album popularity is derived mathematically from track popularity. 
    Note: the popularity value may lag actual popularity by a few days: the value is not updated in real time.
    https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-tracks
    """
    Popularity = "popularity"  # this is not from audio feature. this is from the track itself.
    # ArtistSeparation = 9  # Don't know what those map to


class FullTrack(object):
    def __init__(self, track: FullPlaylistTrack, audio_features: AudioFeatures):
        self.track: FullPlaylistTrack = track
        self.audio_features: AudioFeatures = audio_features
        self.title = track.name
        self.album = track.album.name
        self.artist = track.artists[0]
        self.artists = track.artists


def _extract_track_from_paginated(paginated_tracks: PlaylistTrackPaging) \
        -> list[FullPlaylistTrack | LocalPlaylistTrack | FullPlaylistEpisode | None]:
    return [item.track for item in paginated_tracks.items]


def extract_uri_from_tracks(tracks: Union[List[FullTrack], List[FullPlaylistTrack]]) -> List[str]:
    uris = []
    for track in tracks:
        uris.append(track.uri if isinstance(track, FullPlaylistTrack) else track.track.uri)

    return uris


def get_all_tracks_from_playlist(spotify: Spotify, playlist_id: str) -> List[FullPlaylistTrack]:
    tracks: List[FullPlaylistTrack] = []
    paginated_tracks = spotify.playlist_items(playlist_id)
    tracks.extend(_extract_track_from_paginated(paginated_tracks))
    while len(tracks) < paginated_tracks.total:
        print(f"Tracks found: {len(tracks)}...", end="\r", flush=True)
        paginated_tracks = spotify.playlist_items(playlist_id, offset=len(tracks))
        tracks.extend(_extract_track_from_paginated(paginated_tracks))

    print(f"Total Tracks for this playlist: {len(tracks)}.")
    return tracks


def append_audio_features(spotify: Spotify, tracks: List[FullPlaylistTrack]) -> List[FullTrack]:
    track_ids = [track.id for track in tracks]
    max_ids_per_request = 100
    tracks_plus_audio_features: List[FullTrack] = []
    data_set = [spotify.tracks_audio_features(chunked_track_ids)
                for chunked_track_ids in split_in_chunks(track_ids, max_ids_per_request)]

    for audio_features in data_set:
        for audio_feature in audio_features:
            tracks_plus_audio_features.append(FullTrack(
                track=[track for track in tracks if track.id == audio_feature.id][0],
                audio_features=audio_feature
            ))

        print(f"Fetched audio features for {len(tracks_plus_audio_features)} tracks.", end="\r")

    print(f"Finished fetching audio features for {len(tracks_plus_audio_features)} tracks.")
    return tracks_plus_audio_features


def _get_target_obj(track: FullTrack, attribute: AudioAttribute) -> any:
    return track.track if attribute == AudioAttribute.Popularity else track.audio_features


def _sort_obj(track: FullTrack, attribute: AudioAttribute) -> any:
    return getattr(_get_target_obj(track, attribute), attribute.value)


def sort_list_by_attribute(tracks: List[FullTrack], attribute: AudioAttribute, reverse: bool) -> List[FullTrack]:
    sort_func = partial(_sort_obj, attribute=attribute)
    sorted_list = sorted(tracks, key=sort_func, reverse=reverse)
    return sorted_list
