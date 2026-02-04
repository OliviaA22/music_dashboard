import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import network as netwrk

st.set_page_config(page_title="Collaborator Network", layout="wide")

if st.session_state.selected_artist is None:
    st.warning("Please select an artist from the sidebar")
    st.stop()

contributor_df = pd.read_parquet("data/contributer_data.parquet")

artist_name = st.session_state.selected_artist
artist_id = st.session_state.artist_id
artist_songs = st.session_state.existing_song_df[
    st.session_state.existing_song_df['artist_id'] == artist_id
]

st.title(f"🕸️ {artist_name}'s Collaboration Network")

song_ids = artist_songs['song_id'].tolist()
artist_contributors = contributor_df[contributor_df['song_id'].isin(song_ids)]

tab1, tab2, tab3, tab4 = st.tabs([
    "🎭 By Role", 
    "🤝 Frequent Collaborators", 
    "🏢 Record Labels",
    "🕸️ Network Graph"
])


with tab1:
    st.subheader("Contributions by Role")
    role_counts = artist_contributors.groupby('label').agg({
        'artist_name': 'nunique',
        'song_id': 'nunique'
    }).reset_index()
    role_counts.columns = ['Role', 'Total Contributors', 'Songs Involved']
    role_counts = role_counts.sort_values('Total Contributors', ascending=False)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.dataframe(role_counts, width='stretch', hide_index=True)
    
    with col2:
        fig = px.bar(
            role_counts,
            x='Total Contributors',
            y='Role',
            orientation='h',
            title='Contributor Distribution by Role',
            text='Total Contributors',
            color='Total Contributors',
            color_continuous_scale='Teal'
        )
        fig.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            showlegend=False,
            height=400
        )
        fig.update_traces(textposition='outside')
        st.plotly_chart(fig, width='stretch')
    st.divider()
    
    st.subheader("Explore by Role")
    selected_role = st.selectbox("Select a role", role_counts['Role'].tolist())
    
    role_contributors = artist_contributors[artist_contributors['label'] == selected_role]
    
    role_details = role_contributors.merge(
        artist_songs[['song_id', 'title', 'release_date', 'pageviews']],
        on='song_id'
    )
    
    contributor_summary = role_details.groupby('artist_name').agg({
        'song_id': 'count',
        'pageviews': 'sum'
    }).reset_index()
    contributor_summary.columns = ['Contributor', 'Songs', 'Total Views']
    contributor_summary = contributor_summary.sort_values('Songs', ascending=False)
    
    st.dataframe(contributor_summary, width='stretch', hide_index=True)


with tab2:
    st.subheader("Most Frequent Collaborators")
    
    all_collaborators = artist_contributors.groupby('artist_name').agg({
        'song_id': 'nunique',
        'label': lambda x: ', '.join(sorted(set(x)))
    }).reset_index()
    all_collaborators.columns = ['Collaborator', 'Songs Together', 'Roles']
    all_collaborators = all_collaborators.sort_values('Songs Together', ascending=False)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Unique Collaborators",
            len(all_collaborators)
        )
    
    with col2:
        st.metric(
            "Most Frequent Collaborator",
            all_collaborators.iloc[0]['Collaborator'] if len(all_collaborators) > 0 else "N/A"
        )
    
    with col3:
        st.metric(
            "Max Collaborations",
            all_collaborators.iloc[0]['Songs Together'] if len(all_collaborators) > 0 else 0
        )
    st.divider()
    
    top_20 = all_collaborators.head(20)
    
    fig = px.bar(
        top_20,
        x='Songs Together',
        y='Collaborator',
        orientation='h',
        title='Top 20 Most Frequent Collaborators',
        text='Songs Together'
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, width='stretch')
    st.divider()
    
    st.subheader("Collaboration Details")
    selected_collaborator = st.selectbox(
        "Select collaborator",
        all_collaborators['Collaborator'].tolist()
    )
    
    collab_songs = artist_contributors[
        artist_contributors['artist_name'] == selected_collaborator
    ].merge(
        artist_songs[['song_id', 'title', 'release_date', 'pageviews']],
        on='song_id'
    )
    
    st.dataframe(
        collab_songs[['title', 'label', 'release_date', 'pageviews']],
        width='stretch',
        hide_index=True,
        column_config={
            'title': 'Song',
            'label': 'Role',
            'release_date': 'Release Date',
            'pageviews': st.column_config.NumberColumn('Views', format="%d")
        }
    )


with tab3:
    st.subheader("🏢 Roles Distribution Analysis")
    role_timeline = artist_contributors.merge(
        artist_songs[['song_id', 'release_date']],
        on='song_id'
    )
    
    if 'release_date' in role_timeline.columns:
        role_timeline['release_date'] = pd.to_datetime(
            role_timeline['release_date'], 
            errors='coerce'
        )
        role_timeline['year'] = role_timeline['release_date'].dt.year
        
        roles_per_year = role_timeline.groupby(['year', 'label']).size().reset_index(name='count')
        
        fig = px.line(
            roles_per_year,
            x='year',
            y='count',
            color='label',
            title='Contributor Roles Over Time',
            markers=True
        )
        st.plotly_chart(fig, width='stretch')
    st.divider()
    
    role_diversity = artist_contributors.groupby('song_id').agg({
        'label': lambda x: len(set(x)),
        'artist_name': 'count'
    }).reset_index()
    role_diversity.columns = ['song_id', 'unique_roles', 'total_contributors']
    role_diversity = role_diversity.merge(
        artist_songs[['song_id', 'title', 'pageviews']],
        on='song_id'
    )
    
    st.subheader("Songs by Contributor Diversity")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("Most Contributors")
        top_collab = role_diversity.nlargest(10, 'total_contributors')
        st.dataframe(
            top_collab[['title', 'total_contributors', 'unique_roles']],
            width='stretch',
            hide_index=True
        )
    
    with col2:
        fig = px.scatter(
            role_diversity,
            x='total_contributors',
            y='pageviews',
            hover_data=['title'],
            title='Contributors vs. Page Views'
        )
        st.plotly_chart(fig, width='stretch')


with tab4:
    st.subheader("Collaboration Network Visualization")
    network_type = st.radio(
        "Network View",
        options=["All Collaborators", "By Role"],
        horizontal=True
    )
    
    if network_type == "All Collaborators":
        stats = netwrk.render_full_network(
            artist_name, 
            artist_songs, 
            contributor_df,
            max_nodes=50
        )
    else:
        available_roles = sorted(
            contributor_df[contributor_df['song_id'].isin(artist_songs['song_id'])]['label'].unique()
        )
        selected_role = st.selectbox("Select Role to Visualize", options=available_roles)
        
        netwrk.render_role_network(
            artist_name,
            artist_songs,
            contributor_df,
            selected_role
        )
