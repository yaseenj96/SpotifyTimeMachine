## Spotify Time Capsule - Create Spotify playlists based on specified date & Billboard top 100
## Data scrapes Billboard Top 100 for week and uses Spotify API to create playlist

from bs4 import BeautifulSoup

import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "playlist-modify-private"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                    client_id= '8ebaa659c71d4c508ec63ad55c48cd4a',
                                                    client_secret='a9c1c446c9ab423593b075955abbb447',
                                                    redirect_uri='http://example.com',
                                                    username='125459156',
                                                    show_dialog=True,
                                                    cache_path="token.txt"))


# results = spotify.current_user_saved_tracks()
# user_id = spotify.current_user()
# print(user_id)

daterequested = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD:")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{daterequested}")

billboard100 = response.text
soup = BeautifulSoup(billboard100, "html.parser")

# songs = soup.find_all(id = "title-of-a-story")
songs = soup.select("li ul li h3")

songlist = [song.getText().strip() for song in songs]

print(songlist)

user_id = spotify.current_user()["id"]
print(f"the user id is: {user_id}")

uris = []
for song in songlist[:50]:
    print(song)
    song_result = spotify.search(f"track:{song}", type="track")
    print(song_result)
    try:
        uri = song_result["tracks"]["items"][0]["uri"]
        uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlistname = f"{daterequested} Top 50"
playlist = spotify.user_playlist_create(user_id, playlistname, public=False,description=f"Billboard top 50 from {daterequested}")
playlist_updated = spotify.user_playlist_add_tracks(user_id, playlist["id"],uris)