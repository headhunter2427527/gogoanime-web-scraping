from bs4 import BeautifulSoup
import requests
import pickle as pk
import time
import concurrent.futures

with open('list', 'rb') as f:
    animes = pk.load(f)

DOMAIN = "https://gogoanime.so"

t1 = time.perf_counter()

def getDetails(anime):
    source = requests.get(DOMAIN+animes[anime]["pageLink"]).text

    soup = BeautifulSoup(source, 'lxml')

    details = soup.find('div', class_='anime_info_body_bg')

    p = details.find_all('p', class_='type')

    for detail in p:
        heading = detail.span.text.split(':')
        if animes[anime][heading[0]]:
            continue
        else:
            if detail.a:
                a = detail.find_all('a')
                for link in a:
                    value = link.text.split(',')
                    if not value[0]:
                        animes[anime][heading[0]].append(value[1].strip())
                    else:
                        if(len(a)>1):
                            animes[anime][heading[0]] = [value[0].strip()]
                        else:
                            animes[anime][heading[0]] = value[0].strip()
            else:
                try:
                    animes[anime][heading[0]] = detail.contents[1]
                except Exception as e:
                    pass

    episode = soup.find('div', class_='anime_video_body')

    totalEp = episode.find('a', class_='active')
    totalEpisodes = totalEp['ep_end']

    animes[anime]["Total Episodes"] = totalEpisodes

    print(f"{anime} details completed...")

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = [executor.submit(getDetails, anime) for anime in animes.keys()]

t2 = time.perf_counter()

print(f"Total time taken : {t2-t1} seconds...")

with open('list', 'ab') as f:
    pk.dump(animes, f)
