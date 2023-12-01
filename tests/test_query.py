#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 17:47:19 2023

@author: moritz
"""

from src.utils import ROOT_PATH
from src import query as qry


def test_single_duration():
    with open(ROOT_PATH / "src" / "oscars.sparql", "r") as file:
        query = file.read()
    data = qry.query_wikidata(query)

    df = qry.wikidata_to_df(data)

    assert len(df.n_durations.unique()) == 1
