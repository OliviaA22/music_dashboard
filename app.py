import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv
from genius_client import GeniusClient
import utils as ut


load_dotenv()

TOKEN = os.getenv("TOKEN")
client = GeniusClient(TOKEN)


st.set_page_config(
    page_title="Music Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize session state for navigation and data persistence
if 'selected_artist' not in st.session_state:
    st.session_state.selected_artist = None
if 'artist_id' not in st.session_state:
    st.session_state.artist_id = None
if 'existing_artist_df' not in st.session_state:
    st.session_state.existing_artist_df = pd.read_parquet("data/artist_data.parquet")
if 'existing_song_df' not in st.session_state:
    st.session_state.existing_song_df = pd.read_parquet("data/song_data.parquet")
if 'existing_contributor_df' not in st.session_state:
        st.session_state.existing_contributor_df = pd.read_parquet("data/contributer_data.parquet")

# Pages
overview_page = st.Page("pages/overview.py", title="Artist Overview", icon="🎵")
songs_page = st.Page("pages/songs.py", title="Song Details", icon="🎤")
collaborators_page = st.Page("pages/collaborators.py", title="Collaborator Network", icon="🕸️")
credits_page = st.Page("pages/credits.py", title="Song Credits", icon="🎬")


# Navigation
pg = st.navigation([overview_page, songs_page, collaborators_page, credits_page], position="top")

with st.sidebar:
    st.title("🎵 Select Artist")
    
    available_artists = sorted(
        st.session_state.existing_artist_df['name'].unique().tolist()
    )
    
    selected_artist = st.selectbox(
        "Search for Artist Name", 
        options=available_artists,
        accept_new_options=True,
        index=available_artists.index(st.session_state.selected_artist) if st.session_state.selected_artist in available_artists else 0,
        key='artist_selector'
    )
    
    is_new_artist = selected_artist not in available_artists

    if is_new_artist:
        st.divider()
        fetch_contributors = st.checkbox(
            "Fetch contributors", 
            value=True, 
            help="Takes 2-5 minutes. Uncheck for faster artist loading."
        )
    else:
        fetch_contributors = False

    if selected_artist != st.session_state.selected_artist:
        st.session_state.selected_artist = selected_artist
        new_artist_id = ut.load_or_fetch_artist(
            selected_artist, 
            fetch_contributors=fetch_contributors
        )
        st.session_state.artist_id = new_artist_id
        
        if is_new_artist and new_artist_id is not None:
            st.rerun()
    
    if st.session_state.selected_artist and st.session_state.artist_id:
        artist_row = st.session_state.existing_artist_df[
            st.session_state.existing_artist_df['name'] == st.session_state.selected_artist
        ]
        if not artist_row.empty:
            st.divider()
            img_url = artist_row.iloc[0].get('header_image_url')
            if img_url:
                st.image(img_url, caption=st.session_state.selected_artist)
    
pg.run()
