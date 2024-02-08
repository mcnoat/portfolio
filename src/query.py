# -*- coding: utf-8 -*-
"""
Created on Wed Nov  8 17:38:57 2023

@author: Moritz Schubert
"""

# standard library
from datetime import datetime
from itertools import groupby, count
import string
import time
from typing import Literal

# Python package index
import pandas as pd
import requests

# custom scripts
from src.utils import ROOT_PATH
from src import utils


def query_wikidata(query: str):
    url = "https://query.wikidata.org/sparql"
    data = requests.get(url, params={"query": query, "format": "json"}).json()

    return data


def specify_award(query: str, award: Literal["bear", "lion", "oscar", "palm"]) -> str:
    template = string.Template(query)
    award_id_dict = utils.load_json("awards.json")
    award_id = award_id_dict[award]["id"]
    query = template.substitute(award=award_id)

    return query


def wikidata_to_json(data: dict):
    json = []
    values = [{key: value["value"] for key, value in entry.items()} for entry in data]
    old_wd_id = None
    for v in values["results"]["bindings"]:

        wd_id: str = v["film"].split("/")[-1]
        name: str = v["filmLabel"]
        director_name: str = v["directorLabel"]
        director_gender: str = v["genderLabel"]
        director_dict: dict = {"name": director_name, "gender": director_gender}
        duration: int = int(v["duration"]["value"])

        if wd_id != old_wd_id:
            json.append(
                {"name": name, "duration": duration, "director": [director_dict]}
            )
            old_wd_id = wd_id
        else:
            json[-1]["director"].append(director_dict)

    return json


def consecutive_parts(number_list: list[int]) -> list:
    """Split a list into parts where each part contains consecutive numbers.

    Parameters:
    - lst (list): The input list.

    Returns:
    list of lists: A list of sublists where each sublist contains consecutive numbers.
    """
    result = [
        list(group)
        for key, group in groupby(
            number_list, lambda number, c=count(): number - next(c)
        )
    ]

    return result


def join_duplicates(df: pd.DataFrame):
    """find the duplicate film IDs and join them into single rows"""
    
    result_df = df.groupby("id").agg(lambda x: "/".join(set(x))).reset_index()

    for index in result_df.index:
        title = result_df.loc[index, "title"]
        if "/" in result_df.loc[index, "duration"]:
            raise ValueError(
                f"More than one duration for {title}. Go to WikiData and assign a preferred rang."
            )

    result_df = adjust_datatypes(result_df)

    return result_df


def adjust_datatypes(df: pd.DataFrame):

    integer_columns = ["duration", "year_awarded"]
    for integer_column in integer_columns:
        df[integer_column] = df[integer_column].astype(float).apply(round)

    return df


def check_df_for_completion(df: pd.DataFrame, award: str):
    last_year = datetime.now().year - 1

    if str(last_year) not in df.year_awarded.values:
        raise ValueError(f"Last year's award is missing for {award}")
    
    if df["country"].isna().any():
        raise TypeError(f"There's a film without a country for {award}")


def wikidata_to_df(data: dict) -> pd.DataFrame:
    values = [
        {key: value["value"] for key, value in entry.items()}
        for entry in data["results"]["bindings"]
    ]
    df = pd.DataFrame()

    for i, v in enumerate(values):
        for key in v:
            if key == "film":
                v[key] = v[key].split("/")[-1]
            df.loc[i, key] = v[key]
    
    df = df.rename(columns={"filmLabel": "title",
                    "film": "id",
                    "directorLabel": "director",
                    "genderLabel": "gender",
                    "year": "year_awarded",
                    "countryLabel": "country",
                    "countryCode": "country_code"})

    return df


if __name__ == "__main__":
    awards = list(utils.load_json("awards.json"))

    for award in awards:
        print(f"Processing {award}...")
        with open("query.sparql", "r") as file:
            query_unspecified = file.read()
        query_specified = specify_award(query_unspecified, award)
        data = query_wikidata(query_specified)
        time.sleep(1)

        df_raw = wikidata_to_df(data)
        check_df_for_completion(df_raw, award)
        df_cleaned = join_duplicates(df_raw)
        df_sorted = df_cleaned.sort_values(by="year_awarded", ascending=True)

        results_dir = ROOT_PATH / "results"
        assert results_dir.exists()
        df_sorted.to_csv(results_dir / f"{award}.csv", index=False, encoding="utf8")
