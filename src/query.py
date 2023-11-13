# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:38:57 2023

@author: Moritz Schubert
"""

# Python package index
import jmespath
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
    for d in data["results"]["bindings"]:
        name: str = d["filmLabel"]["value"]
        duration: int = int(d["duration"]["value"])
        #director: str = d["directorLabel"]["value"]
        
        if json and json[-1]["name"] == name:
            print("This should not happen")
            print(json[-1]["name"])
        json.append({"name": name,
                     "duration": duration})
    
    return json
        

if __name__ == "__main__":
    with open("oscars.sparql", "r") as file:
        query = file.read()
    data = query_wikidata(query)
    json = wikidata_to_json(data)
    results_dir = ROOT_PATH / "results"
    assert results_dir.exists()
    utils.dump_json(json, results_dir / "oscars.json")
