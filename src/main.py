#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 20:43:48 2022

@author: moritz
"""

# %% import

# Python package index
import pandas as pd
import requests

# custom scripts
from src.utils import ROOT_PATH

# %% single data point
id_df = pd.read_csv(ROOT_PATH / "data" / "movies.csv")
wikidata_ids = id_df.loc[:, "id"]
ids_str = ""

for wikidata_id in wikidata_ids:
    ids_str += f"wd:{wikidata_id} "

query = f"""
SELECT ?filmLabel ?duration ?directorLabel ?film ?gender_of_directorLabel ?countryLabel ?continentLabel
WHERE {{
    VALUES ?film {{ {ids_str} }}
    OPTIONAL {{?film wdt:P57 ?director.
               ?film wdt:P2047 ?duration.
               ?director wdt:P21 ?gender_of_director.
               ?film wdt:P495 ?country.
               ?country wdt:P30 ?continent.}}

    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
  }}
"""
with open("query.txt", "w") as query_file:
    query_file.write(query)

url = "https://query.wikidata.org/sparql"

data = requests.get(url, params={"query": query, "format": "json"}).json()
df = pd.DataFrame()
id_to_index = {}

for datum in data["results"]["bindings"]:
    # preserve original ordering of the movies
    item_id = datum["film"]["value"].split("/")[-1]
    i_list = id_df.loc[id_df.id == item_id, "id"].index
    i = i_list[0]  # [0], because index returns a list, we want the only element in it
    i += 1  # naturally readable index, i.e. starts at 1 instead of 0

    # populate columns
    df.loc[i, "name"] = datum["filmLabel"]["value"]
    df.loc[i, "director"] = datum["directorLabel"]["value"]
    df.loc[i, "duration"] = datum["duration"]["value"]
    df.loc[i, "gender_of_director"] = datum["gender_of_directorLabel"]["value"]
    df.loc[i, "country"] = datum["countryLabel"]["value"]
    df.loc[i, "continent"] = datum["continentLabel"]["value"]

df.sort_index(inplace=True)
df.to_csv("movie_data.csv")

# %%

genre_query = f"""
SELECT ?item ?itemLabel ?genreLabel
WHERE {{
    VALUES ?item {{ {ids_str} }}
    OPTIONAL {{ ?item wdt:P136 ?genre. }}
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
}}
"""

genre_data = requests.get(url, params={"query": genre_query, "format": "json"}).json()
genre_df = pd.DataFrame()

for i, datum in enumerate(genre_data["results"]["bindings"]):
    # populate columns
    genre_df.loc[i, "name"] = datum["itemLabel"]["value"]
    genre_df.loc[i, "genre"] = datum["genreLabel"]["value"]

genre_df.sort_index(inplace=True)
