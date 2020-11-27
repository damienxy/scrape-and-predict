from typing import List, Dict


# Folder structure:
# <basepath>/<artist>/overview.txt
# <basepath>/<artist>/lyrics/<title>.txt
basepath: str = './temp'
overview_file: str = '/overview.txt'
baseurl: str = 'https://www.lyrics.com'

df_columns: List[str] = ['artist', 'title', 'lyrics']

messages: Dict[str, str] = {
    'welcome': """
    Hello, welcome to 'Guess the artist'! 
    The rules of the game: 
        1. Provide at least two of your favorite artists.
        2. Data will be collected and analysed.
        3. Insert a song line and I will tell you which artist it is from.
    """,
    'provide_artist': 'Please provide an artist or band or write "done":\n',
    'provide_another_artist': 'Please provide another artist or band or write "done"\n',
    'try_again': 'Please provide another artist:\n',
    'artist_not_found': 'Artist not found. Please try again.',
    'site_not_reached': 'Could not reach site. Please try again.',
    'download_interrupted': 'Download interrupted. Prediction will be worse now :-)\n',
    'not_enough_data': 'Not enough data to do anything useful. Bye!',
    'one_more_needed': 'You need to provide one more artist for the programme to work.'
}
