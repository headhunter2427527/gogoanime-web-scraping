from bs4 import BeautifulSoup
import requests
import pickle as pk
import time
import concurrent.futures

t1 = time.perf_counter()

animes = {}

def getList(sourceLink):
    source = requests.get(sourceLink).text

    soup = BeautifulSoup(source, 'lxml')

    ul = soup.find('ul', class_='listing')

    for li in ul.find_all('li'):
        anime = li.a

        name = anime.text
        link = anime['href']

        animes[name] = {}
        animes[name]["pageLink"] = link

    print(f"Page : {sourceLink.split('=')[1]} completed...")


with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(getList, f"https://gogoanime.so/anime-list.html?page={page}") for page in range(1,61)]


print(f"Total animes found: {len(animes)}")

t2 = time.perf_counter()

print(f"Total time taken : {t2-t1} seconds...")

with open('list', 'ab') as f:
    pk.dump(animes, f)
