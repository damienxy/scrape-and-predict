import pathlib
import requests
import itertools
from typing import List, Tuple

from bs4 import BeautifulSoup  # type: ignore

import cfg


def search_artist(artist: str):
    print('Searching for', artist, '...')
    response = requests.get(cfg.baseurl + '/lyrics/' + artist)

    if response.status_code == 200:
        page = BeautifulSoup(response.text, features="lxml")
        if artist_found(page):
            artist_url = get_artist_url(page)
            return artist_url
        else:
            print(cfg.messages['artist_not_found'])
            return search_artist(input(cfg.messages['try_again']))
    else:
        print(cfg.messages['site_not_reached'])
        return search_artist(input(cfg.messages['try_again']))


def artist_found(page) -> bool:
    if page.find('h4', text='We couldn\'t find any lyrics matching your query.'):
        return False
    else:
        return True


def get_artist_url(page) -> str:
    try:
        artist_section = page.find('h3', text='Artists:').parent
        # returns first in artist list
        return artist_section.find('a').get('href')
    except:
        print(cfg.messages['artist_not_found'])
        return search_artist(input(cfg.messages['try_again']))


def make_artist_dir(artist: str) -> Tuple[str, str]:
    artistpath = cfg.basepath + '/' + artist
    lyricpath = artistpath + '/lyrics'
    pathlib.Path(lyricpath).mkdir(parents=True, exist_ok=True)
    return artistpath, lyricpath


def get_artist_overview(artisturl: str, artistpath: str) -> str:
    print('Accessing artist info...')
    response = requests.get(cfg.baseurl + '/' + artisturl)
    if response.status_code == 200:
        overview = response.text
        with open(artistpath + cfg.overview_file, 'w', encoding='utf-8') as f:
            f.write(overview)
            return overview
    else:
        print(cfg.messages['site_not_reached'])
        return search_artist(input(cfg.messages['try_again']))


def extract_links(artisturl: str, overview: str) -> List[str]:
    print('Collecting song links...')
    page = BeautifulSoup(overview, features="lxml")
    # match hrefs starting with /lyric
    hrefs = page.select("a[href^='/lyric']")
    res = [href.get('href') for href in hrefs]
    # remove duplicates
    res_sorted = sorted([x.split('/')
                         for x in res], key=lambda x: x[-1].lower())
    res_grouped = [list(v) for k, v in itertools.groupby(
        res_sorted, lambda x: x[-1].lower())]
    res_unique = [group[0] for group in res_grouped]
    print('Found', len(res_unique), 'songs.')
    # for x in res_unique:
    #     print(x)
    return res_unique
