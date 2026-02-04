import streamlit as st
import pandas as pd

st.set_page_config(page_title="Song Credits", layout="wide")

# ============ CHECK IF ARTIST IS SELECTED ============
if st.session_state.selected_artist is None or st.session_state.artist_id is None:
    st.warning("Please select an artist from the sidebar")
    st.stop()
# ===================================================

artist_name = st.session_state.selected_artist
artist_id = st.session_state.artist_id

st.title(f"🎬 {artist_name}'s Song Credits")

contributor_df = pd.read_parquet("data/contributer_data.parquet")
song_df = st.session_state.existing_song_df
artist_df = st.session_state.existing_artist_df

# ============ FILTER TO SELECTED ARTIST'S SONGS ONLY ============
artist_songs = song_df[song_df['artist_id'] == artist_id].copy()

if len(artist_songs) == 0:
    st.info(f"No songs found for {artist_name}")
    st.stop()

# Get song IDs for this artist
song_ids = artist_songs['song_id'].tolist()

# Filter contributors to only this artist's songs
artist_contributors = contributor_df[contributor_df['song_id'].isin(song_ids)]

if len(artist_contributors) == 0:
    st.info(f"No contributor data available for {artist_name}")
    st.stop()
# ===============================================================

# Merge contributor data with song info
full_credits = artist_contributors.merge(
    artist_songs[['song_id', 'title', 'release_date', 'pageviews']],
    on='song_id'
)

# Show metrics
col_m1, col_m2, col_m3 = st.columns(3)
with col_m1:
    st.metric("Total Songs", len(artist_songs))
with col_m2:
    st.metric("Total Credits", len(full_credits))
with col_m3:
    st.metric("Unique Contributors", full_credits['artist_name'].nunique())

st.divider()

# Search and filter controls
col1, col2, col3 = st.columns(3)

with col1:
    search_song = st.text_input("🔍 Search by Song Title")

with col2:
    search_contributor = st.text_input("🔍 Search by Contributor Name")

with col3:
    role_filter = st.multiselect(
        "Filter by Role",
        options=sorted(artist_contributors['label'].unique())
    )

filtered_credits = full_credits.copy()

if search_song:
    filtered_credits = filtered_credits[
        filtered_credits['title'].str.contains(search_song, case=False, na=False)
    ]

if search_contributor:
    filtered_credits = filtered_credits[
        filtered_credits['artist_name'].str.contains(search_contributor, case=False, na=False)
    ]

if role_filter:
    filtered_credits = filtered_credits[
        filtered_credits['label'].isin(role_filter)
    ]

st.subheader(f"Found {len(filtered_credits)} credits")

st.dataframe(
    filtered_credits[[
        'title', 
        'artist_name', 
        'label', 
        'release_date', 
        'pageviews'
    ]],
    width='stretch',
    hide_index=True,
    column_config={
        'title': 'Song',
        'artist_name': 'Contributor',
        'label': 'Role',
        'release_date': 'Release Date',
        'pageviews': st.column_config.NumberColumn('Views', format="%d")
    }
)
