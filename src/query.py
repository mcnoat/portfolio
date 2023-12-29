# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:38:57 2023

@author: Moritz Schubert
"""

# Python package index
import requests

# custom scripts
from src import utils
from src.utils import ROOT_PATH


def query_wikidata(query: str):
    url = "https://query.wikidata.org/sparql"
    data = requests.get(url, params={"query": query, "format": "json"}).json()

    return data

def wikidata_to_json(data: dict):
    json = []
    values = [{key: value["value"]
               for key, value in entry.items()}
               for entry in data]
    old_wd_id = None
    for v in values["results"]["bindings"]:
        
        if "versionLabel" in v:
            cut = v["versionLabel"]
            if cut =="director's cut":
                continue
        
        wd_id: str = v["film"].split("/")[-1]
        name: str = v["filmLabel"]
        director_name: str = v["directorLabel"]
        director_gender: str = v["genderLabel"]
        director_dict: dict = {"name": director_name,
                               "gender": director_gender}
        duration: int = int(v["duration"]["value"])
        
        if wd_id != old_wd_id:
            json.append({"name": name,
                         "duration": duration,
                         "director": [director_dict]})
            old_wd_id = wd_id
        else:
            json[-1]["director"].append(director_dict)
    
    return json


if __name__ == "__main__":
    with open("oscars.sparql", "r") as file:
        query = file.read()
    data = query_wikidata(query)
        
    json = wikidata_to_json(data)
    results_dir = ROOT_PATH / "results"
    assert results_dir.exists()
    utils.dump_json(json, results_dir / "oscars.json")
