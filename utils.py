import os
import streamlit as st
import pandas as pd
import json
import time
from dotenv import load_dotenv
from genius_client import GeniusClient
import data_prep as dp
import data_update as du


load_dotenv()


TOKEN = os.getenv("TOKEN")
client = GeniusClient(TOKEN)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



def get_artist_id_from_local(artist_name):
    """Get artist ID from local data without API call"""
    existing_artist = st.session_state.existing_artist_df[
        st.session_state.existing_artist_df['name'].str.lower() == artist_name.lower()
    ]
    
    if not existing_artist.empty:
        return existing_artist.iloc[0]['artist_id']
    return None

def load_or_fetch_artist(artist_name, fetch_contributors=True):
    """Load artist from local data or fetch from API if not found"""
    
    artist_id = get_artist_id_from_local(artist_name)
    
    if artist_id is not None:
        return artist_id
    
    with st.spinner(f'🔍 Searching for {artist_name}...'):
        try:
            artist_id = client.get_artist_id(artist_name)
        except Exception as e:
            st.error(f"Could not find artist '{artist_name}': {e}")
            return None

    if artist_id in st.session_state.existing_artist_df['artist_id'].values:
        return artist_id

    with st.spinner(f'Fetching {artist_name} data from Genius API...'):
        try:
            new_artist_df = dp.prep_artist_data(client, artist_name, update_artist_data=False)
            new_artist_song_df = dp.prep_artist_song_data(client, artist_name, update_artist_song_data=False)

            if new_artist_df.empty:
                st.warning(f"No artist data found for '{artist_name}'")
                return None
            
            # Datatype conversion
            new_artist_song_df = new_artist_song_df.copy()
            if 'release_date' in new_artist_song_df.columns:
                new_artist_song_df['release_date'] = pd.to_datetime(
                    new_artist_song_df['release_date'], 
                    errors='coerce'
                )
            
            problematic_cols = ['release_date_components', 'stats', 'featured_artists', 'primary_artist']
            
            for col in problematic_cols:
                if col in new_artist_song_df.columns:
                    new_artist_song_df[col] = new_artist_song_df[col].apply(
                        lambda x: json.dumps(x) if isinstance(x, (dict, list)) else None
                    )
            
            existing_columns = st.session_state.existing_song_df.columns.tolist()
            new_artist_song_df = new_artist_song_df.reindex(columns=existing_columns)

            du.update_artist_data(new_artist_df)
            du.update_artist_song_data(new_artist_song_df)
            # Fetch contributors if requested
            contributor_count = 0
            if fetch_contributors:
                with st.spinner(f'🎵 Fetching contributors for {artist_name}...'):
                    contributor_count = fetch_and_update_contributors(artist_name, new_artist_song_df)
            
            # Update session state
            st.session_state.existing_artist_df = pd.concat(
                [st.session_state.existing_artist_df, new_artist_df], 
                ignore_index=True
            )
            st.session_state.existing_song_df = pd.concat(
                [st.session_state.existing_song_df, new_artist_song_df], 
                ignore_index=True
            )
            
            if contributor_count > 0:
                st.success(f"✅ Successfully added {artist_name} with {contributor_count} collaborators!")
            else:
                st.success(f"✅ Successfully added {artist_name}!")
            
        except Exception as e:
            st.error(f"Error fetching artist data")
            st.info("💡 Tips:\n- Check artist name spelling\n- Try the exact name from Genius.com")
            return None
    
    return artist_id


def fetch_and_update_contributors(artist_name, song_df):
    """
    Fetch contributor data for an artist's songs
    
    Args:
        artist_name: Name of the artist
        song_df: DataFrame containing song_id column
        
    Returns:
        int: Number of unique collaborators found, or 0 if none
    """
    all_contributors = []
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    song_ids = song_df['song_id'].tolist()
    total_songs = len(song_ids)
    
    for idx, song_id in enumerate(song_ids):
        try:
            contributors = dp.prep_contributer_data(client, song_id)
            
            if len(contributors) > 0:
                all_contributors.append(contributors)
            
            progress_bar.progress((idx + 1) / total_songs)
            status_text.text(f"Processing {idx + 1}/{total_songs} songs...")
            
            time.sleep(0.7)
            
        except KeyError:
            time.sleep(0.3)
        except Exception:
            time.sleep(0.3)
            continue
    
    progress_bar.empty()
    status_text.empty()
    
    if all_contributors:
        contributor_df = pd.concat(all_contributors, ignore_index=True)
        contributor_df = contributor_df.drop_duplicates()
        
        du.update_contributer_data(contributor_df)
        
        if 'existing_contributor_df' in st.session_state:
            st.session_state.existing_contributor_df = pd.concat(
                [st.session_state.existing_contributor_df, contributor_df],
                ignore_index=True
            ).drop_duplicates()
        
        return contributor_df['artist_name'].nunique()
    
    return 0