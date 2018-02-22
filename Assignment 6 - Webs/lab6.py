import requests
from bs4 import BeautifulSoup
import re

page = requests.get('https://www.olympic.org/pyeongchang-2018/results/en/general/nocs-list.htm')
soup = BeautifulSoup(page.content, 'lxml')
countries = soup.find('div', class_='CountriesList')
countries_text = countries.get_text()
countries_list = [x for x in countries_text.split("\n") if x.strip()!='']
print(countries_list)

first_letter = input('First letter of Country Name: ')
print('Countries participating in the Winter Olympics:')

choice_list = []
for i, j in enumerate(countries_list, 1):
    if j.startswith(first_letter.upper()):
        choice_list.append(j)
        print(('{}: {}').format(i,j))

choice = input('Type in a number: ')
print(('Data for {}').format(choice_list[int(choice)-1]))