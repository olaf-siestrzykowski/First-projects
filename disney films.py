import pickle

import pandas.io.json
from bs4 import BeautifulSoup as bs
import requests
"""
toy_story_url = "https://en.wikipedia.org/wiki/Toy_Story_3"

r = requests.get(toy_story_url)

soup = bs(r.content)

contents = soup.prettify()
info_box = soup.find(class_="infobox vevent")
info_rows = info_box.find_all("tr")
#for row in info_rows:
    #print(row.prettify())

def get_content_value(row_data):
    if row_data.find("li"):
        return [li.get_text(" ", strip=True).replace("\xa0", " ") for li in row_data.find_all("li")]
    elif row_data.find("br"):
        return [text for text in row_data.stripped_strings]
    else:
        return row_data.get_text(" ", strip=True).replace("\xa0", " ")

movie_info = {}
for index, row in enumerate(info_rows):
    if index == 0:
        movie_info["title"] = row.find("th").get_text(" ", strip=True)
    elif index == 1:
        continue
    else:
        content_key = row.find("th").get_text(" ", strip=True)
        content_value = get_content_value(row.find("td"))
        movie_info[content_key] = content_value

pixar_url = "https://en.wikipedia.org/wiki/List_of_Walt_Disney_Pictures_films"

rr = requests.get(pixar_url)

soup2 = bs(rr.content)

movies = soup2.select(".wikitable.sortable i a")

base_path = "https://en.wikipedia.org/"
movie_info_list = []


def clean_tags(soup):
    for tag in soup.find_all(["sup", "span"]):
        tag.decompose()


def get_info_box(url):
    r = requests.get(url)
    soup = bs(r.content)
    contents = soup.prettify()
    info_box = soup.find(class_="infobox vevent")
    info_rows = info_box.find_all("tr")
    clean_tags(soup)

    movie_info = {}
    for index, row in enumerate(info_rows):
        if index == 0:
            movie_info['title'] = row.find("th").get_text(" ", strip=True)
        else:
            header = row.find('th')
            if header:
                content_key = row.find("th").get_text(" ", strip=True)
                content_value = get_content_value(row.find("td"))
                movie_info[content_key] = content_value
    return movie_info
"""
"""for index, movie in enumerate(movies):
    try:
        relative_path = movie["href"]
        title = movie["title"]
        full_path = base_path + relative_path
        movie_info_list.append(get_info_box(full_path))
    except Exception as e:
        print(movie.get_text())
        print(e)
"""
# print(movie_info_list)

import json


def save_data(title, data):
    with open(title, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_data(title):
    with open(title, "r", encoding="utf-8") as f:
        return json.load(f)


"""print(len(movie_info_list))
save_data("disney_data.json", movie_info_list)"""

loaded_movie_info_list = load_data("disney_data.json")

# print([movie.get("Running time", "N/A") for movie in loaded_movie_info_list])


def minutes_to_int(running_time):
    if running_time == "N/A":
        return None
    if isinstance(running_time, list):
        entry = running_time[0]
        return int(entry.split(" ")[0])
    else:
        return int(running_time.split(" ")[0])


for movie in loaded_movie_info_list:
    movie["Running time (int)"] = minutes_to_int(movie.get("Running time", "N/A"))

# print([movie.get("Running time (int)", "N/A") for movie in loaded_movie_info_list])
import moneyconvert

for movie in loaded_movie_info_list:
    movie["Budget (float)"] = moneyconvert.money_conversion(movie.get("Budget", "N/A"))
    movie["Box office (float)"] = moneyconvert.money_conversion(movie.get("Box office", "N/A"))

# print(loaded_movie_info_list[44])

# print([movie.get("Release date", "N/A") for movie in loaded_movie_info_list])

# 1950–present

from datetime import datetime


def clean_date(date):
    return date.split("(")[0].strip()


def date_conversion(date):
    if isinstance(date, list):
        date = date[0]

    if date == "N/A":
        return None
    date_str = clean_date(date)

    fmts = ["%B %d, %Y", "%B %d %Y", "%d %B %Y"]
    for fmt in fmts:
        try:
            return datetime.strptime(date_str, fmt)
        except:
            pass
    return None


dates = [movie.get("Release date", "N/A") for movie in loaded_movie_info_list]

for movie in loaded_movie_info_list:
    movie["Release date (datetime)"] = date_conversion(movie.get("Release date", "N/A"))

# print(loaded_movie_info_list[56])

import pickle


def save_data_pickle(name, data):
    with open(name, "wb") as f:
        pickle.dump(data, f)


def load_data_pickle(name):
    with open(name, "rb") as handle:
        return pickle.load(handle)

# save_data_pickle("disney_movie_cleaned_data", loaded_movie_info_list)


movie_info_list = load_data_pickle("disney_movie_cleaned_data")

# print(movie_info_list[6])

import requests
import urllib

api_key = "65e02a38"


def get_omdb_info(title):
    base_url = "http://www.omdbapi.com/?"
    parameters = {"apikey": api_key, "t": title}
    params_encoded = urllib.parse.urlencode(parameters)
    full_url = base_url + params_encoded
    return requests.get(full_url).json()


def get_rotten_tomato(omdb_info):
    ratings = omdb_info.get("Ratings", [])
    for rating in ratings:
        if rating["Source"] == "Rotten Tomatoes":
            return rating["Value"]
    return None


"""
for movie in movie_info_list:
    title = movie["title"]
    omdb_info = get_omdb_info(title)
    movie["imdb"] = omdb_info.get("imdbRating", None)
    movie["Metascore"] = omdb_info.get("Metascore", None)
    movie["Rotten Tomatoes"] = get_rotten_tomato(omdb_info)

save_data_pickle("disney_movie_final.pickle", movie_info_list)
"""

movie_info_list2 = load_data_pickle("disney_movie_final.pickle")
print(movie_info_list2[50])

movie_info_copy = [movie.copy() for movie in movie_info_list2]

for movie in movie_info_copy:
    current_date = movie["Release date (datetime)"]
    if current_date:
        movie["Release date (datetime)"] = current_date.strftime("%B %d, %Y")
    else:
        movie["Release date (datetime)"] = None

# save_data("disney_final_data.json", movie_info_copy)

# Save to csv
import pandas as pd

df = pd.DataFrame(movie_info_list2)

# df.to_csv("disney_movie_final.csv")

running_time = df.sort_values(["Budget (float)"], ascending=False)
print(running_time.head(15))