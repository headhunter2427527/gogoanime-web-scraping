from bs4 import BeautifulSoup
import requests
import pickle as pk

animes = {}

for i in range(1,61):
    source = requests.get(f"https://gogoanime.so/anime-list.html?page={i}").text

    soup = BeautifulSoup(source, 'lxml')

    ul = soup.find('ul', class_='listing')

    for li in ul.find_all('li'):
        anime = li.a

        name = anime.text
        link = anime['href']

        animes[name] = link

with open('list', 'ab') as f:
    pk.dump(animes, f)
