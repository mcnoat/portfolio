#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 18:00:22 2023

@author: moritz
"""

# Python package index
import numpy as np
import pandas as pd


def calculate_gender_ratio(genders: str) -> float:
    genders_lst = genders.split(",")
    genders_nums = [0 if gender == "male" else 1 for gender in genders_lst]
    ratio = round(np.mean(genders_nums), 2)

    return ratio


def assign_gender_ratio(df: pd.DataFrame) -> pd.DataFrame:
    for i, gender_str in enumerate(df.genders):
        df.loc[i, "gender_ratio"] = calculate_gender_ratio(gender_str)

    return df
