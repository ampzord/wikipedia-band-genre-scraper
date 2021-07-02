#!/usr/bin/env python

"""
The area of interest of each wikipedia page is inside a TABLE tag always. (https://i.imgur.com/WlGLraM.png)
After, each row is defined by a TR(Table Row) tag.
Where in TH(Table Header) we have the header of the information displayed afterwards in a TD(Table Data).
"""

import requests
import re
from bs4 import BeautifulSoup


response = requests.get(
	url="https://en.wikipedia.org/wiki/Metallica",
)

soup = BeautifulSoup(response.content, 'html.parser')

wiki_tables = soup.find_all('table')

for table in wiki_tables:
	rows = table.find_all('tr')

	for row in rows:
		curr_row = row.find_all('th', string='Genres')

		if len(curr_row) > 0:
			print(row) #original row
			print()
			#print(row.next_element.contents)
			#print(row.next_element.next_element.next_element)

