# -*- coding: utf-8 -*-
import os
from pathlib import Path
import tekore as tk
from tekore import RefreshingToken, Spotify

client_id = os.environ.get("SPOTIFY_CLIENT_ID")
client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")
redirect_uri = 'https://example.com/callback'
config_file = "tekore.cfg"


def authenticate() -> RefreshingToken:
    user_token = tk.prompt_for_user_token(
        client_id,
        client_secret,
        redirect_uri,
        scope=tk.scope.every
    )

    conf = (client_id, client_secret, redirect_uri, user_token.refresh_token)
    tk.config_to_file(config_file, conf)
    return user_token


def get_auth_from_cache() -> RefreshingToken:
    conf = tk.config_from_file(config_file, return_refresh=True)
    user_token = tk.refresh_user_token(*conf[:2], conf[3])
    return user_token


def has_auth_cache() -> bool:
    return Path(config_file).exists()


def get_spotify() -> Spotify:
    token = get_auth_from_cache() if has_auth_cache() else authenticate()
    spotify = tk.Spotify(token)
    return spotify
