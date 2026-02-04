import json
import pandas as pd

def update_artist_data(new_artist_df):
    parquet_path = "data/artist_data.parquet"
    csv_path = "data/artist_data.csv"

    existing_df = pd.read_parquet(parquet_path)
    
    if new_artist_df['artist_id'].isin(existing_df['artist_id']).any():
        print("Artist already in data")
        return existing_df
    
    combined_df = pd.concat([existing_df, new_artist_df], ignore_index=True)

    combined_df.to_parquet(parquet_path, index=False)
    combined_df.to_csv(csv_path, index=False, sep=";")

    return combined_df.dropna(subset=["artist_id"])


def update_artist_song_data(new_artist_song_df):  
    parquet_path = "data/song_data.parquet"
    csv_path = "data/song_data.csv"

    existing_df = pd.read_parquet(parquet_path)
    
    problematic_cols = ['release_date_components', 'stats', 'featured_artists', 'primary_artist']
    new_artist_song_df = new_artist_song_df.copy()
    
    for col in problematic_cols:
        if col in new_artist_song_df.columns:
            new_artist_song_df[col] = new_artist_song_df[col].apply(
                lambda x: json.dumps(x) if isinstance(x, (dict, list)) else None
            )
    
    for col in problematic_cols:
        if col in existing_df.columns:
            existing_df[col] = existing_df[col].apply(
                lambda x: json.dumps(x) if isinstance(x, (dict, list)) 
                         else x if isinstance(x, str) 
                         else None
            )

    new_rows = new_artist_song_df[~new_artist_song_df['song_id'].isin(existing_df['song_id'])]
    if new_rows.empty:
        print("No new songs to add")
        return existing_df

    combined_df = pd.concat([existing_df, new_rows], ignore_index=True)
    combined_df.to_parquet(parquet_path, index=False)
    combined_df.to_csv(csv_path, index=False, sep=";")

    return combined_df


def update_artist_song_data_old(new_artist_song_df):
    parquet_path = "data/song_data.parquet"
    csv_path = "data/song_data.csv"

    existing_df = pd.read_parquet(parquet_path)

    new_rows = new_artist_song_df[~new_artist_song_df['song_id'].isin(existing_df['song_id'])]
    if new_rows.empty:
        print("No new songs to add")
        return existing_df

    combined_df = pd.concat([existing_df, new_rows], ignore_index=True)
    combined_df.to_parquet(parquet_path, index=False)
    combined_df.to_csv(csv_path, index=False, sep=";")

    return combined_df

def update_contributer_data(new_cont_df):
    parquet_path = "data/contributer_data.parquet"
    csv_path = "data/contributer_data.csv"

    existing_df = pd.read_parquet(parquet_path)

    new_rows = new_cont_df[~new_cont_df['song_id'].isin(existing_df['song_id'])]
    if new_rows.empty:
        print("No new songs to add")
        return existing_df

    combined_df = pd.concat([existing_df, new_rows], ignore_index=True)
    combined_df.to_parquet(parquet_path, index=False)
    combined_df.to_csv(csv_path, index=False, sep=";")

    return combined_df