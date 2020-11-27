import re

import pandas as pd  # type: ignore

import artist as a
import lyrics as l
import cfg


def collect_artists(df, message):
    while True:
        artist = input(message)

        if artist in ['', 'done']:
            if len(df['artist'].unique()) < 2:
                print(cfg.messages['one_more_needed'])
                pass
            else:
                collect_artists = False
                return df
        else:
            df = add_artist(df, artist)


def add_artist(df, artist: str):
    # Search artist and get artist URL
    artisturl = a.search_artist(artist)

    # Create relevant directories if they don't exist yet
    artist_lowercase = re.sub('\W', '', artist).lower()
    artistpath, lyricpath = a.make_artist_dir(artist_lowercase)

    # Scrape overview page and extract song links
    overview = a.get_artist_overview(artisturl, artistpath)
    links = a.extract_links(artisturl, overview)

    # Check which lyrics exist yet
    remaining_links = l.get_remaining_download_links(links, lyricpath)

    # Scrape and extract lyrics
    l.scrape_lyrics_pages(remaining_links, lyricpath)
    rows = l.extract_lyrics(lyricpath)

    # Add lyrics data to dataframe
    new_df = add_to_df(df, rows)
    new_df = remove_duplicates(new_df, ['title', 'artist'])
    print('Currently in database:')
    print(new_df['artist'].value_counts())
    print()

    return new_df


def add_to_df(df, rows):
    print('Adding', len(rows), 'songs to corpus...')
    new_df = pd.DataFrame(rows, columns=['artist', 'title', 'lyrics'])
    new_df = clean_df(new_df)
    return df.append(new_df, ignore_index=True)


def clean_df(df):
    print('Removing duplicates...')
    # remove other artists
    df = df[df['artist'] == df['artist'].mode()[0]]
    # remove title duplicates
    df = remove_duplicates(df, 'title')
    # remove '\n' chars from strings
    df['lyrics'] = [re.sub('\\n', ' ', row) for row in df['lyrics']]
    return df


def remove_duplicates(df, subset=['title', 'artist']):
    df = df.drop_duplicates(subset=subset)
    return df
