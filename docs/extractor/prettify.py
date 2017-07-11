'''bs prettify'''
from bs4 import BeautifulSoup


soup = BeautifulSoup(open('698OI.html', encoding='utf-8'), "html.parser")

with open('698OI.html', 'w', encoding='utf-8') as file_to_w:
    file_to_w.write(soup.prettify())
