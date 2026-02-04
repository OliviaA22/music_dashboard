# Music Artist Dashboard

The dashboard is an interactive data visualization application that enables you to explore an artists discography with a special focus on their collaborators. It is built using the data retrieved via the [Genius Developer API](https://docs.genius.com/). 

## Getting Started

### Installing

* To run the dashboard, clone this repository onto your local machine and install all necessary dependencies compiled in the requirements.txt.
```
pip install -r requirements.txt
```

### Executing program

* To open the streamlit dashboard, simply run
```
streamlit run app.py
```

## Data Retrieval

### Genius Client (genius_client.py)

This files has the code for initializing a client class by taking the API secret as a parameter. It furthermore holds multiple functions, each responsible for connecting to one of the several API endpoints provided by Genius.

#### get_artist_id()

Every API call, either for artist or song, requires a Genius specific id as a parameter. To still enable the user to enter the name of an artist of their choice, this could be mitigated by calling the [search endpoint](https://docs.genius.com/#search-h2). This endpoint mirrors the internal search of the Genius website and when an artist is entered, it returns songs of that specific artist. In addition to the general song data, each song also returns data for the primary artist. We therefore iterate over the returned songs until the first one where the entered artist matches the primary artist of the song (case insensitive) and return the ID from there.

Although case insensitive, if the artist is entered with a wrong spelling it can not be promised to work. A fallback is added in which the first songs primary artist is returned in case no matches can be found.

#### get_song_data()
This function takes a song ID and calls the [song endpoint](https://docs.genius.com/#songs-h2) and returns the data as a json.

#### get_artist_data()

This function takes a artist ID and calls the [artist endpoint](https://docs.genius.com/#artists-h2) and returns the data as a json.

#### get_artist_songs()

This function takes an artist ID as well but calls an extension of the artist endpoint with which the songs of an artist can be batch retrieved. By default only 20 songs for an artist are returned, but the page can be added as a parameter, so the function calls itself recursively until the variable "next_page" is empty.

In comparison to the song endpoint, this returns much less variables and although it is used to retrieve all necessary song IDs for the selected artists, it can not be used as a stand in or a batch download alternative for the song data endpoint.

### Data Preparation

This file defines multiple functions that call the client, then parse over the returned json format and prepare / clean it for further processing.

### Data Update

This file defines functions for updating the separate parquet files for the dashboard, to make sure there are no unnecessary API calls being made and the data is clean before saving.

## Data Architecture

The data is stored in and in the dashboard code called from local parquet files. In addition to that it is also saved as CSVs for debugging reasons, but those are not directly used in the code and just serve for human oversight purposes.

### Artist Data

This file holds all the necessary data that is retrieved from the artist endpoint, for example 'name', 'description' (if available), 'header_image', etc.

### Song Data

Counterintuitively the data in this file is not retrieved by the song data endpoint, but the extended artist songs endpoint. 

### Contributer Data

The contributer data is retrieved from the song data endpoint and holds the name, id and label for every artist involved in the making of each song (also including people that worked on the music video).

## Dashboard Code

### Main App

### Network Code

### Utils





## Known Bugs

### Reselecting the artist

### 