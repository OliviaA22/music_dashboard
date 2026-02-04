import pandas as pd
import data_update as du


# --- Genius Data Preparation ---

def prep_artist_song_data(client, artist, include_song_data=False, update_artist_song_data=True):
    artist_id = client.get_artist_id(artist)
    artist_song_json = client.get_artist_songs(artist, num_returned=50, page=1)['response']['songs']
    artist_song_df = pd.DataFrame(artist_song_json)

    artist_song_df = artist_song_df.rename(columns={'id': 'song_id'})
    artist_song_df['artist_id'] = artist_id
    #artist_song_df['release_date'] = pd.to_datetime(artist_song_df['release_date_components'].apply(pd.Series), errors='coerce')
    
    components = artist_song_df['release_date_components'].apply(pd.Series)
    artist_song_df['release_date'] = pd.to_datetime(
        components[['year', 'month', 'day']],
        errors='coerce'
    )

    # Stat Dictionary
    stats = pd.json_normalize(artist_song_df['stats'])
    artist_song_df['hot'] = stats['hot']
    try:
        artist_song_df['pageviews'] = stats['pageviews']
    except:
        artist_song_df['pageviews'] = 0

    artist_song_df['pageviews'] = artist_song_df['pageviews'].fillna(0)

    columns = ['song_id', 'title', 'api_path', 'artist_names', 'artist_id', 'full_title',
       'header_image_thumbnail_url', 'header_image_url', 
       'primary_artist_names',
       'relationships_index_url', 'release_date_components', 'release_date',
       'song_art_image_thumbnail_url', 'song_art_image_url', 'stats', 'hot', 'pageviews',
       'url', 'featured_artists', 'primary_artist']
    
    if update_artist_song_data == True:
        du.update_artist_song_data(artist_song_df[columns])
    
    song_data = []
    
    if include_song_data == True:
        for song_id in artist_song_df['song_id']:
            song_data_df = prep_song_data(client, song_id)
            song_data.append(song_data_df)

        song_features_df = pd.concat(song_data, ignore_index=True)

        return artist_song_df[columns], song_features_df
    
    return artist_song_df[columns]


def prep_artist_data(client, artist, include_artist_song_data=False, include_song_data=False, update_artist_data=True):
    artist_json = client.get_artist_data(artist)['response']['artist']
    artist_df = pd.DataFrame([artist_json])

    artist_df = artist_df.rename(columns={'id': 'artist_id'})
    artist_df['description'] = artist_df['description'].apply(lambda x: x['plain'])

    columns = ['artist_id', 'name', 'description', 'alternate_names', 'header_image_url', 'image_url', 'social_links', 'followers_count']

    artist_df = artist_df[columns].drop_duplicates(['artist_id'])

    if update_artist_data == True:
        du.update_artist_data(artist_df)

    return artist_df


def prep_song_data(client, song_id):
    song_json = client.get_song_data(song_id)['response']['song']
    song_df = pd.DataFrame([song_json])
    song_df = song_df.rename(columns={'id': 'song_id'})
    
    # Description
    song_df['description'] = song_df['description'].apply(lambda x: x['plain'])

    # Artist
    song_df['primary_artist_id'] = client.get_artist_id(song_df['primary_artist_names'][0])

    # Stat Dictionary
    stats = pd.json_normalize(song_df['stats'])
    song_df['hot'] = stats['hot']
    try:
        song_df['pageviews'] = stats['pageviews']
    except:
        song_df['pageviews'] = 0

    # Album Dictionary
    album = pd.json_normalize(song_df['album'])

    try: 
        song_df['album_id'] = album['id']
        song_df['album_title'] = album['name']
        song_df['album_cover_art_url'] = album['cover_art_url']
    except:
        song_df['album_id'] = "None"
        song_df['album_title'] = "None"
        song_df['album_cover_art_url'] = "None"


    # Collaborator Dictionary
    colab = pd.json_normalize(song_df['custom_performances'])
    
    exploded = song_df.explode('custom_performances')
    normalized = pd.json_normalize(exploded['custom_performances'])

    print(normalized.columns)

    columns = ['song_id', 'title', 'description', 'primary_artist_id', 'primary_artist_names', 'language', 'recording_location', 'release_date', 'hot', 'pageviews', 'song_art_primary_color', 'song_art_secondary_color', 'album_id', 'album_title', 'album_cover_art_url']

    return song_df[columns]


def prep_contributer_data(client, song_id):
    song_json = client.get_song_data(song_id)['response']['song']
    song_df = pd.DataFrame([song_json])
    song_df = song_df.rename(columns={'id': 'song_id'})

    tmp = song_df[['custom_performances']].explode('custom_performances')
    perf_df = pd.json_normalize(tmp['custom_performances'])
    perf_df = perf_df.explode('artists')
    artist_df = pd.json_normalize(perf_df['artists'])

    result_df = pd.DataFrame({
        'label': perf_df['label'].values,
        'artist_id': artist_df['id'].values,
        'artist_name': artist_df['name'].values
    })

    rows = []

    for artists in song_df['writer_artists']:
        for artist in artists:
            rows.append({
                'label': 'Writer',
                'artist_id': artist.get('id'),
                'artist_name': artist.get('name')
            })

    writer_df = pd.DataFrame(rows)

    rows = []

    for artists in song_df['producer_artists']:
        for artist in artists:
            rows.append({
                'label': 'Producer',
                'artist_id': artist.get('id'),
                'artist_name': artist.get('name')
            })

    producer_df = pd.DataFrame(rows)

    final_df = pd.concat([result_df, writer_df, producer_df], ignore_index=True)
    final_df['song_id'] = song_id

    return final_df[['song_id', 'artist_id', 'artist_name', 'label']]






