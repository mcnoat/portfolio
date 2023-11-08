# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:38:57 2023

@author: Moritz Schubert
"""

# Python package index
import pandas as pd
import requests

# custom scripts
from src.utils import ROOT_PATH

def query_wikidata(query: str):
    url = "https://query.wikidata.org/sparql"
    data = requests.get(url, params={"query": query, "format": "json"}).json()
    
    return data


def wikidata_to_df(data: dict):
    df = pd.DataFrame({"name": pd.Series([], dtype=str),
                       "duration": pd.Series([], dtype=int)})
    for i, datum in enumerate(data["results"]["bindings"]):
        df.loc[i, "name"] = datum["filmLabel"]["value"]
        df.loc[i, "duration"]  = int(datum["duration"]["value"])
    
    return df
        

if __name__ == "__main__":
    with open("oscars.sparql", "r") as file:
        query = file.read()
    data = query_wikidata(query)
    df = wikidata_to_df(data)
    results_dir = ROOT_PATH / "results"
    assert results_dir.exists()
    df.to_csv(results_dir / "oscars.csv", index=False)
