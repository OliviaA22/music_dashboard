import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Song Details", layout="wide")

if st.session_state.selected_artist is None:
    st.warning("Please select an artist from the sidebar")
    st.stop()

if st.session_state.artist_id is None:
    st.error("Artist ID not found")
    st.stop()

artist_name = st.session_state.selected_artist
artist_id = st.session_state.artist_id
artist_songs = st.session_state.existing_song_df[
    st.session_state.existing_song_df['artist_id'] == artist_id
].copy()

st.title(f"📀 {artist_name}'s Discography")
if len(artist_songs) == 0:
    st.warning(f"No songs found for {artist_name}")
    st.stop()

col1, col2, col3 = st.columns(3)

with col1:
    sort_by = st.selectbox(
        "Sort by",
        options=["Release Date", "Page Views", "Title"],
        index=0
    )

with col2:
    sort_order = st.radio("Order", options=["Descending", "Ascending"], horizontal=True)

with col3:
    if 'release_date' in artist_songs.columns:
        artist_songs['release_date'] = pd.to_datetime(artist_songs['release_date'], errors='coerce')
        valid_dates = artist_songs['release_date'].dropna()
        if len(valid_dates) > 0:
            min_year = int(valid_dates.min().year)
            max_year = int(valid_dates.max().year)
            year_filter = st.slider("Filter by Year", min_year, max_year, (min_year, max_year))
        else:
            year_filter = (2000, 2026)
    else:
        year_filter = (2000, 2026)

sort_column_map = {
    "Release Date": "release_date",
    "Page Views": "pageviews",
    "Title": "title"
}
ascending = sort_order == "Ascending"

if sort_column_map[sort_by] in artist_songs.columns:
    artist_songs = artist_songs.sort_values(
        by=sort_column_map[sort_by], 
        ascending=ascending,
        na_position='last'
    )

if 'release_date' in artist_songs.columns:
    artist_songs = artist_songs[
        (artist_songs['release_date'].dt.year >= year_filter[0]) &
        (artist_songs['release_date'].dt.year <= year_filter[1])
    ]
st.divider()

cols_per_row = 3
rows = (len(artist_songs) + cols_per_row - 1) // cols_per_row

for row in range(rows):
    cols = st.columns(cols_per_row)
    for col_idx in range(cols_per_row):
        song_idx = row * cols_per_row + col_idx
        if song_idx < len(artist_songs):
            song = artist_songs.iloc[song_idx]
            
            with cols[col_idx]:
                with st.container(border=True):
                    if pd.notna(song.get('album_cover_art_url')):
                        st.image(song['album_cover_art_url'], width='stretch')

                    st.subheader(song['title'])

                    if pd.notna(song.get('release_date')):
                        try:
                            st.caption(f"📅 {pd.to_datetime(song['release_date']).strftime('%B %d, %Y')}")
                        except:
                            st.caption(f"📅 {song['release_date']}")

                    if pd.notna(song.get('pageviews')):
                        st.metric("Views", f"{int(song['pageviews']):,}")
