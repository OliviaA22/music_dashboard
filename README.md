
# 🎵 Music Analytics Dashboard

A comprehensive Streamlit-based interactive dashboard for analyzing music artist data from the Genius API. Visualize artist metrics, track popularity, explore collaborations, and dive deep into song analytics.

![Dashboard Preview](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)

---

## 📋 Table of Contents

- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Data Sources](#data-sources)
- [API Reference](#api-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 📊 Core Analytics
- **Artist Overview**: Total songs, views, followers, and engagement metrics
- **Top Hits Dashboard**: Visual ranking of an artist's most popular songs
- **Release Timeline**: Interactive lollipop chart showing song releases over time
- **Collaborator Network**: Network graph visualization of artist collaborations

### 🎯 Key Metrics
- Total song count
- Aggregate pageviews
- Average views per song
- Artist follower count
- Hot track indicators
- Lyrical annotation depth

### 🔍 Interactive Features
- Dynamic artist search and selection
- Real-time data filtering
- Cached data loading for performance
- Automatic parsing of nested JSON structures
- Responsive layout with custom CSS styling

### 🚀 Performance Optimizations
- Streamlit caching for fast data access
- One-time data parsing at startup
- Minimal API calls (uses pre-fetched data)
- Efficient DataFrame operations

---

## 🎬 Demo

### Dashboard Overview
```
┌─────────────────────────────────────────────────────────┐
│  [Artist Name]'s Overview                               │
├─────────────┬─────────────┬─────────────┬──────────────┤
│ Total Songs │ Total Views │ Avg Views   │ 🔥 Followers │
│     247     │  12.5M      │   50,607    │    8,369     │
├─────────────────────────────────────────────────────────┤
│  🕸️ Collaborator Network  │  🏆 Top Hits              │
│                            │  1. Song Title (1.2M)     │
│   [Network Graph]          │  2. Song Title (980K)     │
│                            │  3. Song Title (850K)     │
│                            │  4. Song Title (720K)     │
│                            │  5. Song Title (650K)     │
├─────────────────────────────────────────────────────────┤
│  📅 Release History                                     │
│  [Interactive Timeline Chart]                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/music-analytics-dashboard.git
cd music-analytics-dashboard
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create Required Files
```bash
# Create data directory
mkdir -p data

# Create style file
touch style.css

# Create environment file
touch .env
```

---

## ⚙️ Configuration

### 1. Genius API Token

Create a `.env` file in the project root:

```env
TOKEN=your_genius_api_token_here
```

**How to get a Genius API token:**
1. Visit [Genius API Clients](https://genius.com/api-clients)
2. Sign in or create an account
3. Create a new API Client
4. Copy your Client Access Token
5. Paste it in the `.env` file

### 2. Data Files

Place your data files in the `data/` directory:
```
data/
├── artist_data.parquet
└── song_data.parquet
```

**Expected Data Structure:**

**artist_data.parquet:**
```
artist_id | name | description | alternate_names | header_image_url | image_url | social_links | followers_count
----------|------|-------------|-----------------|------------------|-----------|--------------|----------------
1233909   | ...  | ...         | ...             | ...              | ...       | ...          | 8369
```

**song_data.parquet:**
```
song_id | title | primary_artist_id | primary_artist_names | release_date | stats | album_cover_art_url | ...
--------|-------|-------------------|---------------------|--------------|-------|---------------------|----
378195  | ...   | 16775             | Artist Name         | 2014-03-17   | {...} | https://...         | ...
```

### 3. Custom Styling

Edit `style.css` to customize the dashboard appearance:

```css
/* Example custom styles */
.stApp {
    background-color: #0E1117;
}

.metric-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
}

/* Add your custom CSS here */
```

---

## 🚀 Usage

### Starting the Dashboard

```bash
streamlit run draft.py
```

The dashboard will open automatically in your browser at `http://localhost:8501`

### Basic Workflow

1. **Select an Artist**: Use the sidebar dropdown to search and select an artist
2. **View Metrics**: See overview statistics in the top row
3. **Explore Collaborations**: Interact with the network graph
4. **Check Top Hits**: View the artist's most popular songs
5. **Analyze Timeline**: Examine release patterns over time

### Adding New Artists

When you select an artist not in the database:
1. The system automatically detects it's a new artist
2. Makes minimal API calls to fetch basic info
3. Parses and caches the data
4. Displays the dashboard immediately

### Performance Tips

- ✅ First load parses all data (may take 10-30 seconds)
- ✅ Subsequent loads are instant (cached)
- ✅ Use existing artists to avoid API rate limits
- ✅ Clear cache if data becomes stale: `st.cache_data.clear()`

---

## 📁 Project Structure

```
music-analytics-dashboard/
│
├── draft.py                    # Main Streamlit application
├── data_prep.py               # Data preparation utilities
├── genius_client.py           # Genius API client wrapper
├── network.py                 # Network visualization module
├── style.css                  # Custom CSS styling
├── .env                       # Environment variables (API keys)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
│
├── data/                      # Data directory
│   ├── artist_data.parquet    # Artist metadata
│   └── song_data.parquet      # Song metadata
│
└── venv/                      # Virtual environment (not tracked)
```

### File Descriptions

| File | Purpose |
|------|---------|
| `draft.py` | Main dashboard application with UI components |
| `data_prep.py` | Functions for data fetching and preprocessing |
| `genius_client.py` | API client for Genius API interactions |
| `network.py` | Collaboration network graph generation |
| `style.css` | Custom CSS for dashboard styling |
| `.env` | Stores API tokens and secrets |

---

## 📊 Data Sources

### Genius API

This project uses the [Genius API](https://docs.genius.com/) to fetch:
- Artist metadata (name, followers, images)
- Song information (title, pageviews, release dates)
- Annotation data (lyric annotations)
- Collaboration data (featured artists)

**API Endpoints Used:**
- `GET /artists/:id` - Artist details
- `GET /artists/:id/songs` - Artist songs
- `GET /songs/:id` - Song details

### Data Schema

**Stats Column Structure** (nested in song_data):
```json
{
  "pageviews": 451239,
  "hot": false,
  "unreviewed_annotations": 1,
  "concurrents": null
}
```

**Primary Artist Column Structure**:
```json
{
  "id": 1233909,
  "name": "Artist Name",
  "image_url": "https://...",
  "is_verified": false
}
```

---

## 🔌 API Reference

### GeniusClient Class

```python
from genius_client import GeniusClient

client = GeniusClient(token="your_api_token")

# Get artist ID by name
artist_id = client.get_artist_id("Artist Name")

# Get artist data
artist_data = client.get_artist_data(artist_id)

# Get song data
song_data = client.get_song_data(song_id)
```

### Data Prep Functions

```python
import data_prep as dp

# Prepare artist song data
artist_songs, song_features = dp.prep_artist_song_data(
    client, 
    "Artist Name",
    include_song_data=False  # Set True for detailed data
)

# Prepare artist metadata
artist_df = dp.prep_artist_data(
    client,
    "Artist Name",
    include_song_data=False
)

# Prepare detailed song data (makes API calls)
song_details = dp.prep_song_data(client, artist_songs)
```

### Network Visualization

```python
import network as netwrk

# Render collaboration network
netwrk.render_mini_network(
    artist_name="Artist Name",
    song_df=existing_song_df
)
```

---

## 🐛 Troubleshooting

### Common Issues

#### 1. `KeyError: 'response'`
**Cause**: API rate limiting or invalid song IDs

**Solution**:
```python
# Use cached data instead of API calls
song_details = artist_songs[['song_id', 'title', 'unreviewed_annotations']].copy()
```

#### 2. `ModuleNotFoundError`
**Cause**: Missing dependencies

**Solution**:
```bash
pip install -r requirements.txt
```

#### 3. Empty Dashboard / No Data
**Cause**: Data not parsed or filtering issue

**Solution**:
```python
# Check if data exists
print(f"Total songs: {len(existing_song_df)}")
print(f"Filtered songs: {len(artist_songs)}")

# Verify parsing
print(artist_songs.columns)
```

#### 4. Slow Performance
**Cause**: Parsing data on every run

**Solution**:
```python
# Ensure caching is enabled
@st.cache_data
def load_and_parse_data():
    # ... parsing logic
```

#### 5. API Rate Limits
**Cause**: Too many API requests

**Solution**:
- Use `include_song_data=False` for new artists
- Rely on pre-fetched CSV data
- Implement request delays: `time.sleep(1)`

### Debug Mode

Add debug prints to diagnose issues:

```python
# At the top of draft.py
DEBUG = True

if DEBUG:
    st.write("Debug Info:")
    st.write(f"Artist ID: {artist_input_id}")
    st.write(f"Artist Songs: {len(artist_songs)}")
    st.write(f"Columns: {artist_songs.columns.tolist()}")
```

---

## 📦 Requirements

```txt
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.17.0
python-dotenv>=1.0.0
requests>=2.31.0
pyarrow>=13.0.0  # For parquet file support
```

**Install all at once:**
```bash
pip install streamlit pandas plotly python-dotenv requests pyarrow
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Reporting Bugs
1. Check if the bug is already reported in [Issues](https://github.com/yourusername/music-analytics-dashboard/issues)
2. Create a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Error messages/screenshots

### Suggesting Features
1. Open a new issue with the `enhancement` label
2. Describe the feature and its benefits
3. Provide mockups if applicable

### Pull Requests
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Write/update tests if applicable
5. Commit with clear messages: `git commit -m "Add feature X"`
6. Push to your fork: `git push origin feature-name`
7. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Use type hints where appropriate
- Keep functions focused and modular

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

## 🙏 Acknowledgments

- **Genius API** - For providing comprehensive music data
- **Streamlit** - For the excellent dashboard framework
- **Plotly** - For interactive visualizations
- **Community Contributors** - Thank you to all who contribute!

---

## 📧 Contact

- **Author**: [Your Name]
- **Email**: your.email@example.com
- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Project Link**: [https://github.com/yourusername/music-analytics-dashboard](https://github.com/yourusername/music-analytics-dashboard)

---

## 🗺️ Roadmap

### Version 1.0 (Current)
- ✅ Basic artist dashboard
- ✅ Top hits visualization
- ✅ Collaboration network
- ✅ Release timeline

### Version 1.1 (Planned)
- [ ] Multi-artist comparison
- [ ] Export to PDF/PNG
- [ ] Advanced filters (by year, genre)
- [ ] Sentiment analysis of lyrics

### Version 2.0 (Future)
- [ ] Real-time streaming data
- [ ] Machine learning predictions
- [ ] Spotify integration
- [ ] User authentication
- [ ] Custom playlist generation

---

## 📊 Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/music-analytics-dashboard?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/music-analytics-dashboard?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/music-analytics-dashboard)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/music-analytics-dashboard)

---

**⭐ If you find this project useful, please consider giving it a star!**

Made with ❤️ and 🎵
