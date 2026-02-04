import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import network as netwrk
from utils import local_css


local_css("style.css")

if st.session_state.selected_artist is None:
    st.warning("Please select an artist from the sidebar")
    st.stop()

if st.session_state.artist_id is None:
    st.error("Artist ID not found. Please reselect the artist.")
    st.stop()

artist_name = st.session_state.selected_artist
artist_id = st.session_state.artist_id

artist_df = st.session_state.existing_artist_df[
    st.session_state.existing_artist_df['artist_id'] == artist_id
]

artist_songs = st.session_state.existing_song_df[
    st.session_state.existing_song_df['artist_id'] == artist_id
].copy()

st.title(f"{artist_name}'s Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.metric("Total Songs", len(artist_songs))

with col2:
    with st.container(border=True):
        total_views = artist_songs['pageviews'].sum() if 'pageviews' in artist_songs.columns else 0
        st.metric("Total Views", f"{int(total_views):,}")

with col3:
    with st.container(border=True):
        if len(artist_songs) > 0 and 'pageviews' in artist_songs.columns:
            avg_views = artist_songs['pageviews'].mean()
            if pd.notna(avg_views):
                st.metric("Avg Views/Song", f"{int(avg_views):,}")
            else:
                st.metric("Avg Views/Song", "N/A")
        else:
            st.metric("Avg Views/Song", "0")

with col4:
    with st.container(border=True):
        artist_followers = artist_df['followers_count'].iloc[0] if not artist_df.empty and 'followers_count' in artist_df.columns else 0
        st.metric("🔥 Followers", f"{int(artist_followers):,}")

row2_col1, row2_col2 = st.columns([2, 1])

with row2_col1:
    with st.container(border=True):
        st.subheader("🕸️ Collaborator Network")
        st.caption("Click to explore detailed collaborations →")
        if st.button("View Full Collaborator Details", key="collab_btn"):
            st.switch_page("pages/collaborators.py")

        try:
            contributor_df = pd.read_parquet("data/contributer_data.parquet")
            netwrk.render_mini_network(artist_name, artist_songs, contributor_df)
        except Exception as e:
            st.info("Contributor data not available yet")
            netwrk.render_mini_network(artist_name, artist_songs)

with row2_col2:
    with st.container(border=True):
        st.subheader("🏆 Top Hits")
        
        if 'pageviews' in artist_songs.columns:
            top_songs = artist_songs.sort_values(by='pageviews', ascending=False).head(5)
        else:
            top_songs = artist_songs.head(5)
        
        for idx, (_, song) in enumerate(top_songs.iterrows()):
            c1, c2 = st.columns([1, 3])
            with c1:
                try:
                    cover_url = song.get('album_cover_art_url')
                    if pd.notna(cover_url):
                        st.image(cover_url, width=50)
                    else:
                        st.write("🎵")
                except Exception:
                    st.write("🎵")
            
            with c2:
                st.caption(song.get('title', 'Unknown'))
                pageviews = song.get('pageviews', 0)
                if pd.notna(pageviews):
                    st.caption(f"👁 {int(pageviews):,} views")
                else:
                    st.caption("👁 N/A views")
            
            if idx < 4:
                st.divider()

with st.container(border=True):
    col_t1, col_t2 = st.columns([4, 1])
    with col_t1:
        st.subheader("📅 Release History")
    with col_t2:
        if st.button("View Details", key="release_btn"):
            st.switch_page("pages/songs.py")
    
    if 'release_date' in artist_songs.columns:
        artist_songs_copy = artist_songs.copy()
        artist_songs_copy['release_date'] = pd.to_datetime(
            artist_songs_copy['release_date'], 
            errors='coerce'
        )
        timeline_df = artist_songs_copy.dropna(subset=['release_date']).sort_values('release_date')
        
        if len(timeline_df) > 0 and 'pageviews' in timeline_df.columns:
            fig = go.Figure()
            
            for _, row in timeline_df.iterrows():
                fig.add_trace(go.Scatter(
                    x=[row['release_date'], row['release_date']],
                    y=[0, row['pageviews']],
                    mode='lines',
                    line=dict(color='rgba(255,75,75,0.3)', width=3),
                    showlegend=False,
                    hoverinfo='none'
                ))
            
            fig.add_trace(go.Scatter(
                x=timeline_df['release_date'],
                y=timeline_df['pageviews'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=timeline_df['pageviews'],
                    colorscale='Plasma',
                    showscale=False
                ),
                text=timeline_df['title'],
                hovertemplate="<b>%{text}</b><br>%{x|%b %Y}<br>Views: %{y:,}<extra></extra>",
                showlegend=False
            ))
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=350,
                xaxis=dict(
                    showgrid=False,
                    showline=True,
                    linecolor='#333',
                    tickfont=dict(color='#888')
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#333',
                    gridwidth=1,
                    tickfont=dict(color='#888'),
                    title="Page Views"
                ),
                margin=dict(l=0, r=0, t=20, b=0)
            )
            st.plotly_chart(fig, width='stretch')
        else:
            st.info("No release date information available")
    else:
        st.warning("No release dates available for timeline.")
