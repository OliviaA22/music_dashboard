import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd
import streamlit as st
import ast


def get_collaborators(main_artist, df_songs, df_contributors=None):
    """
    Extract all collaborators and their metadata.
    Returns: dict with {name: {'count', 'roles', 'songs'}}
    """
    collaborators = {}
    
    if df_contributors is not None:
        song_ids = df_songs['song_id'].tolist()
        song_titles = dict(zip(df_songs['song_id'], df_songs['title']))
        
        artist_contributors = df_contributors[df_contributors['song_id'].isin(song_ids)]
        
        for _, row in artist_contributors.iterrows():
            name = row.get('artist_name')
            role = row.get('label', 'Contributor')
            song_id = row.get('song_id')
            song_title = song_titles.get(song_id, 'Unknown')
            
            if name and name != main_artist:
                if name not in collaborators:
                    collaborators[name] = {'count': 0, 'roles': set(), 'songs': []}
                collaborators[name]['count'] += 1
                collaborators[name]['roles'].add(role)
                if song_title not in collaborators[name]['songs']:
                    collaborators[name]['songs'].append(song_title)
    
    return collaborators


def build_network_graph(main_artist, collaborators, limit=None, show_detailed_hover=False):
    """Build NetworkX graph from collaborator data."""
    G = nx.Graph()
    G.add_node(main_artist, size=40, color="#EAC40A", title=f"{main_artist} - Main Artist")
    
    sorted_collabs = sorted(collaborators.items(), key=lambda x: x[1]['count'], reverse=True)
    if limit:
        sorted_collabs = sorted_collabs[:limit]
    
    for collab_name, data in sorted_collabs:
        count = data['count']
        
        node_size = 40
        
        if show_detailed_hover:
            roles_text = ", ".join(sorted(data['roles'])) if data['roles'] else "Featured Artist"
            songs_preview = "• " + "• ".join(data['songs'][:5])
            if len(data['songs']) > 5:
                songs_preview += f"...and {len(data['songs']) - 5} more"
            hover = f"{collab_name}; {count} collaboration(s); Roles:{roles_text}; Songs:{songs_preview}"
        else:
            hover = f"{collab_name}; {count} collaboration(s)"
        
        G.add_node(collab_name, size=node_size, color="#FF4B4B", title=hover)
        G.add_edge(main_artist, collab_name, weight=10)
    
    return G


def render_network(G, height='300px', filename='graph'):
    """Render NetworkX graph as interactive HTML using PyVis."""
    net = Network(height=height, bgcolor="#1E1E1E", font_color='white')
    net.from_nx(G)
    net.barnes_hut(gravity=-8000, central_gravity=0.3, spring_length=100, spring_strength=0.001)
    
    try:
        path = '/tmp'
        net.save_graph(f'{path}/{filename}.html')
        with open(f'{path}/{filename}.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except:
        net.save_graph(f'{filename}.html')
        with open(f'{filename}.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    components.html(html_content, height=int(height.replace('px', '')) + 10)


def render_mini_network(main_artist, df_songs, df_contributors=None):
    """Compact network for overview card."""
    collaborators = get_collaborators(main_artist, df_songs, df_contributors)
    
    if not collaborators:
        st.info(f"No collaborators found for {main_artist}")
        return
    G = build_network_graph(main_artist, collaborators, limit=15, show_detailed_hover=False)
    render_network(G, height='300px', filename='mini_graph')


def render_full_network(main_artist, df_songs, df_contributors=None, max_nodes=50):
    """Full-page interactive network."""
    if df_contributors is None:
        st.warning("Contributor data required for full network")
        return
    
    collaborators = get_collaborators(main_artist, df_songs, df_contributors)
    
    if not collaborators:
        st.info(f"No collaborators found for {main_artist}")
        return
    
    G = build_network_graph(main_artist, collaborators, limit=max_nodes, show_detailed_hover=True)
    render_network(G, height='600px', filename='full_graph')


def render_role_network(main_artist, df_songs, df_contributors, selected_role=None):
    """Network filtered by contributor role with color coding."""
    if df_contributors is None:
        st.warning("Contributor data required")
        return
    
    song_ids = df_songs['song_id'].tolist()
    artist_contributors = df_contributors[df_contributors['song_id'].isin(song_ids)]
    
    if selected_role:
        artist_contributors = artist_contributors[artist_contributors['label'] == selected_role]
    
    if len(artist_contributors) == 0:
        st.info(f"No contributors found" + (f" with role: {selected_role}" if selected_role else ""))
        return
    
    # Build graph with role-based colors
    G = nx.Graph()
    G.add_node(main_artist, size=35, color="#EAC40A", title=f"{main_artist} - Main Artist")
    
    role_colors = {
        'Producer': '#FFD700', 'Writer': '#00CED1', 'Featured Artist': '#FF69B4',
        'Composer': '#9370DB', 'Engineer': '#32CD32', 'Publisher': '#FFA500'
    }

    contributor_stats = artist_contributors.groupby('artist_name').agg({
        'label': lambda x: ', '.join(sorted(set(x))[:3]),
        'song_id': 'count' 
    }).reset_index()
    contributor_stats.columns = ['artist_name', 'roles', 'count']
    
    for _, row in contributor_stats.iterrows():
        contributor = row['artist_name']
        roles = row['roles']
        count = row['count']
        
        if contributor != main_artist:
            first_role = roles.split(',')[0].strip()
            color = role_colors.get(first_role, '#FF4B4B')
            node_size = 40  
            
            G.add_node(contributor, size=node_size, color=color, 
                      title=f"{contributor}Roles: {roles}{count} credits")

            G.add_edge(main_artist, contributor, weight=10)
    
    render_network(G, height='500px', filename='role_graph')
