import pandas as pd
import json
import requests

class GeniusClient():

    def __init__(self, client_secret):
        self.client_secret = client_secret
        self.base_url = 'https://api.genius.com'


    def get_artist_id(self, input):
        input = input.replace(" ", "%20").lower()
        url = f"{self.base_url}/search?q={input}"
        headers = {"Authorization": f"Bearer {self.client_secret}"}
        params = {"text_format": "plain"}
        r = requests.get(url, headers=headers, params=params)
        hits = r.json()["response"]["hits"]

        for h in hits:
            name = h["result"]["primary_artist"]["name"].replace(" ", "%20").lower()
            if name == input:
                return h["result"]["primary_artist"]["id"]

        return hits[0]["result"]["primary_artist"]["id"] #fallback
    

    def get_song_id(self, song_id):
        return 0


    def get_artist_data(self, artist):
        artist_id = self.get_artist_id(artist)
        url = f"{self.base_url}/artists/{artist_id}"
        headers = {"Authorization": f"Bearer {self.client_secret}"}
        params = {"text_format": "plain"}
        r = requests.get(url, headers=headers, params=params)
        return r.json()
    

    def get_artist_songs(self, artist, num_returned, page, artist_id=None, all_songs=None):
        if all_songs is None:
            all_songs = []

        if artist_id is None:
            artist_id = self.get_artist_id(artist)

        url = f"{self.base_url}/artists/{artist_id}/songs"
        headers = {"Authorization": f"Bearer {self.client_secret}"}
        params = {
            "per_page": num_returned,
            "page": page,
            "sort": "popularity",
            "include_features": False,
            "text_format": "plain"
        }

        r = requests.get(url, headers=headers, params=params)

        if r.status_code != 200:
            raise RuntimeError(
                f"Genius API error {r.status_code}: {r.text[:200]}"
            )

        data = r.json()

        filtered_songs = [
            song for song in data["response"]["songs"]
            if song["primary_artist"]["id"] == artist_id
        ]

        all_songs.extend(filtered_songs)

        next_page = data["response"]["next_page"]

        if next_page:
            return self.get_artist_songs(
                artist,
                num_returned=num_returned,
                page=next_page,
                all_songs=all_songs,
                artist_id=artist_id
            )
        
        return {
            "response": {
                "songs": all_songs
            }
        }

    
    def get_song_data(self, song_id):
        url = f"{self.base_url}/songs/{song_id}"
        headers = {"Authorization": f"Bearer {self.client_secret}"}
        params = {"text_format": "plain"}
        r = requests.get(url, headers=headers, params=params)
        return r.json()