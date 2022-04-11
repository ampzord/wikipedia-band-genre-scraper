#!/usr/bin/env python

"""
The area of interest of each wikipedia page is inside a TABLE tag always. (https://i.imgur.com/WlGLraM.png)
Each row is defined by a TR(Table Row) tag. Where the leftside descriptor is defined as a TH(Table Header)
and the rightside descriptor is defined as a TD(Table Data).
"""

import requests
import re
from bs4 import BeautifulSoup
import string
import pandas as pd

__author__ = "António Pereira"
__email__ = "antonio_m_sp@hotmail.com"
__status__ = "Development"

# Edge Case 1 - Wikipedia page exists but it's unrelated (https://en.wikipedia.org/wiki/Adept) -> https://en.wikipedia.org/wiki/Adept_(band)
# Edge Case 2 - Wikipedia page exists but it's ambiguous (https://en.wikipedia.org/wiki/Ne_obliviscaris)
# Edge Case 3 - Wikipedia page exists, but not of the band
# Edge Case 4 - Wikipedia page doesn't exist (underground band - https://en.wikipedia.org/wiki/Aetherian)


excel_metal_data_df = pd.read_excel('Band Genres.xlsx', sheet_name="Metal Bands")
excel_rock_data_df = pd.read_excel('Band Genres.xlsx', sheet_name="Rock Bands")

excel_metal_band_names = excel_metal_data_df['Bands'].tolist()
excel_rock_band_names = excel_rock_data_df['Bands'].tolist()
URL = "https://en.wikipedia.org/wiki/"


def write_to_csv(band_names, band_genres, csv_name):
    tmp_dict = {'Bands': band_names,
                'Genres': band_genres}

    df = pd.DataFrame(tmp_dict)
    df.to_csv(csv_name, index=False)


def wiki_request(excel_band_names):
    response = requests.get(
        URL + excel_band_names
    )
    return response


def parseGenres(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    wiki_tables = soup.find_all('table')
    band_genres = []

    for table in wiki_tables:
        rows = table.find_all('tr')
        for row in rows:
            tmp_row = row.find_all('th', string='Genres')
            if len(tmp_row) > 0:
                curr_row = row.find_all('a', href=re.compile("/wiki/"))
                for row_genres in curr_row:
                    band_genres.append(string.capwords(row_genres.string))

    return band_genres


def checkForDisambiguationWord(response):
    searched_word = "disambiguation"

    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.body.find_all(string=re.compile('.*{0}.*'.format(searched_word)), recursive=True)

    print("Found disambiguation: ", len(results))


def band_genre_scraper(excel_band_names):
    response = wiki_request(excel_band_names)

    if response.status_code != 200:
        print("No wikipedia page found for band/or incomplete page:", excel_band_names)

    band_genres = parseGenres(response)

    if band_genres:
        band_genres_list.append(band_genres)
    else:
        response = wiki_request(excel_band_names + ' (band)')
        band_genres = parseGenres(response)
        band_genres_list.append(band_genres)


if __name__ == "__main__":
    band_genres_list = []
    for i in range(len(excel_metal_band_names)):
        band_genre_scraper(excel_metal_band_names[i])

    write_to_csv(excel_metal_band_names, band_genres_list, 'metal_genres.csv')

    band_genres_list = []
    for i in range(len(excel_rock_band_names)):
        band_genre_scraper(excel_rock_band_names[i])

    write_to_csv(excel_rock_band_names, band_genres_list, 'rock_genres.csv')





