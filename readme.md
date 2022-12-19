# Spotify Playlist Sorter
This is a couple of re-usable python scripts taht will target a single playlist and create variants for it, sorting
by the audio features that Spotify offers.

## What are those Audio Features?
The following Audio Features available are:
- Acoustic: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
- Danceability: describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
- Length: The duration of the track in milliseconds.
- Energy: Is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
- Instrumental: Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
- Key: The key the track is in. Integers map to pitches using standard Pitch Class notation.
- Live: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
- Loudness: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typically range between -60 and 0 db.
- Mode: Indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.
- Speechiness: Detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
- BeatsPerMinute: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration.
- TimeSignature: An estimated time signature. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure). The time signature ranges from 3 to 7 indicating time signatures of "3/4", to "7/4".
- Valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
- Popularity: The popularity of the track. The value will be between 0 and 100, with 100 being the most popular. The popularity of a track is a value between 0 and 100, with 100 being the most popular. The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are. Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated independently. Artist and album popularity is derived mathematically from track popularity. Note: the popularity value may lag actual popularity by a few days: the value is not updated in real time.
  

References: 
- https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features
- https://developer.spotify.com/documentation/web-api/reference/#/operations/get-several-tracks

## How to use?

1. Install dependencies
```shell
pip install -r requirements.txt
```
2. Register an application in Spotify: https://developer.spotify.com/dashboard/login
3. Create a couple environment variables:
  - `SPOTIFY_CLIENT_ID` containing the client id from the app you registered in the previous step.
  - `SPOTIFY_CLIENT_SECRET` containing the client secret from the app you registered in the previous step.
4. Change the target name of the playlist you want. (`main.py` on line 69)
5. Run `main.py`
6. When you run the script for the first time, it will ask you to authorize this app with you account. After that, a browser window will (https://example.com/callback) open with the callback from the authentication. Copy that url with all parameters and paste it in the terminal. After the first time, you won't need to do this.

Those are all the steps. After that, the first run, a config file will be saved, and we'll use cache the next time.

## What exactly this script will do?
It will search for a specific playlist and create 2 variants (ascending and descending) for each audio feature 
available.

Example of this script at work:
- Original Playlist: 🤘-2022 (https://open.spotify.com/playlist/6XMqwMRw6xHBA14Z8WrsvF?si=e47b248e66a44b80)

After running this script, I got those playlist variants:
- 🤘-2022 - popularity ASC (https://open.spotify.com/playlist/5rrRbqlmHIJGnV7EOVFTZQ)
- 🤘-2022 - popularity DESC (https://open.spotify.com/playlist/2lYwzw3nezfmZOCVkrpzac)
- 🤘-2022 - valence ASC (https://open.spotify.com/playlist/1XY4iGYeoEuowk0G9kxoti)
- 🤘-2022 - valence DESC (https://open.spotify.com/playlist/0ZkGb88SOPwHacMXogcgcJ)
- 🤘-2022 - time signature ASC (https://open.spotify.com/playlist/5smVuFhpPVcF7n5RaS9vQt)
- 🤘-2022 - time signature DESC (https://open.spotify.com/playlist/6yV8v1OSJz4W0hrweVKyxh)
- 🤘-2022 - tempo ASC (https://open.spotify.com/playlist/3IQLvzdqn8zHfqJQlMnljK)
- 🤘-2022 - tempo DESC (https://open.spotify.com/playlist/0wgtctTq01HrXiSzWdfWU7)
- 🤘-2022 - speechiness ASC (https://open.spotify.com/playlist/3r8HDmtbFIVJZzYavctDCK)
- 🤘-2022 - speechiness DESC (https://open.spotify.com/playlist/44vvuf3JnteqYrBunmkRVp)
- 🤘-2022 - mode ASC (https://open.spotify.com/playlist/4hGk8jmQ33gIQ45pJlo6iN)
- 🤘-2022 - mode DESC (https://open.spotify.com/playlist/48q2fftR1jppp6yEpWxZKa)
- 🤘-2022 - loudness ASC (https://open.spotify.com/playlist/5uGZYHik4n8xMzjQELKEan)
- 🤘-2022 - loudness DESC (https://open.spotify.com/playlist/3Om1aH7K7Zc5sXx3rJUnX1)
- 🤘-2022 - liveness ASC (https://open.spotify.com/playlist/2N83oir6XbomHgU70lHN9o)
- 🤘-2022 - liveness DESC (https://open.spotify.com/playlist/3IdPaIH1ucAl0tEsfeT6Em)
- 🤘-2022 - key ASC (https://open.spotify.com/playlist/5ZaJMF4g39qSORqoFe8ssy)
- 🤘-2022 - key DESC (https://open.spotify.com/playlist/6nLD3NzIee3rPjVTUwGHAI)
- 🤘-2022 - instrumentalness ASC (https://open.spotify.com/playlist/7MrbRmlPp7Z15FxMkDEnvf)
- 🤘-2022 - instrumentalness DESC (https://open.spotify.com/playlist/10B3eWFEKesSgB6uukEyFB)
- 🤘-2022 - energy ASC (https://open.spotify.com/playlist/7Agdk2MnZbQK3ZsxJc7ICl)
- 🤘-2022 - energy DESC (https://open.spotify.com/playlist/3WgSRzpBhVRsPOeynm6Ck7)
- 🤘-2022 - duration ms ASC (https://open.spotify.com/playlist/42SdRMigvBT2cYXYKY3wKO)
- 🤘-2022 - duration ms DESC (https://open.spotify.com/playlist/2DGoUfVbkpMt44EOBE3iYX)
- 🤘-2022 - danceability ASC (https://open.spotify.com/playlist/3Bv9uSqRRjgIpvBrlMvr04)
- 🤘-2022 - danceability DESC (https://open.spotify.com/playlist/0sqq0iuaJn3xdi8yiAboOr)
- 🤘-2022 - acousticness ASC (https://open.spotify.com/playlist/7ENtrbg9cjocR1hBb34GJ0)
- 🤘-2022 - acousticness DESC (https://open.spotify.com/playlist/5t72bjBkaKHZJUcY9gMTqu)

## Disclaimer
I created this script to learn a bit about what Spotify API has to offer. Should be safe to use, 
but I offer no guarantees. 
