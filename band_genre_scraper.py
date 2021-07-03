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

# TODO Edge case on wikipedia on url incorrect (example: Architects vs Architects_(band) )
# TODO Edge case on page being empty,
#    and just a redirect to several other pages (example: https://en.wikipedia.org/wiki/Ne_obliviscaris)
# TODO Edge case page wikipedia exists but not of the band


excel_data_df = pd.read_excel('Band Genres.xlsx', sheet_name="Metal Genres")
excel_band_names = excel_data_df['Bands'].tolist()
url = "https://en.wikipedia.org/wiki/"
hasBandTextInURL = False


def band_genre_scraper():
    response = requests.get(
        url + excel_band_names[i]
    )

    if response.status_code != 200:
        webpageExists = False
        print(url + excel_band_names[i] + " - Error response code")
        continue

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

    if band_genres:
        band_genres.sort()
        print(excel_band_names[i] + " - ", end='')
        print(band_genres)
    else:  # list is empty
        hasBandTextInURL = True
        band_genre_scraper()




for i in range(len(excel_band_names)):
    webpageExists = True
    band_genre_scraper()





