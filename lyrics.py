import requests
import os
from typing import List, Tuple

from bs4 import BeautifulSoup  # type: ignore
from tqdm import tqdm  # type: ignore

import cfg


def get_remaining_download_links(links: List[str], lyricpath: str) -> List[str]:
    to_be_downloaded = get_links_to_download(links, lyricpath)
    print('Already downloaded:', len(links) - len(to_be_downloaded))
    print('Left to download:', len(to_be_downloaded))
    return to_be_downloaded


def get_links_to_download(links: List[str], lyricpath: str) -> List[str]:
    filenames = get_filenames(lyricpath)
    links_extended = [(x, x[-1] + '.txt') for x in links]
    linknames = [x[1] for x in links_extended]
    diff = list(set(linknames).difference(filenames))
    return [link[0] for link in links_extended if link[1] in diff]


def get_filenames(path: str):
    return os.listdir(path)


def scrape_lyrics_pages(links: List[str], lyricpath: str):
    print('Scraping lyrics...')
    if links:
        try:
            for link in tqdm(links, leave=True):
                url = cfg.baseurl + '/'.join(link)
                # print(url)
                response = requests.get(url)
                if response.status_code == 200:
                    with open(lyricpath + '/' + link[-1] + '.txt', 'w', encoding='utf-8') as f:
                        f.write(response.text)
                else:
                    print(response.status_code)
            print('Done')
        except KeyboardInterrupt:
            print(cfg.messages['download_interrupted'])


def extract_lyrics(lyricpath: str) -> List[Tuple[str, str, str]]:
    print('Extracting text...')
    results = []
    for fname in tqdm(get_filenames(lyricpath), leave=True):
        with open(lyricpath + '/' + fname, 'r') as f:
            try:
                page = f.read()
                soup = BeautifulSoup(page, features="lxml")
                artist = soup.find(class_='lyric-artist').a.text
                title = soup.find(class_='lyric-title').text
                lyrics = soup.find(class_='lyric-body').text
                results.append((artist, title, lyrics))
            except:
                pass
    return results
