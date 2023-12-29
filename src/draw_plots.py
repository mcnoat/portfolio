#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 23:04:45 2022

@author: moritz
"""

# Python package index
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

# custom scripts
import src.pipes as pps
from src.utils import ROOT_PATH


def plot_duration(df, association_chain: bool = False):
    fig, ax = plt.subplots()
    
    sns.set_theme()
    ax = sns.swarmplot(data=df.duration, orient="h")
    ax.set_xlabel("duration [min]")

    if association_chain:
        current_movie = df.tail(1)
        current_hist, _ = np.histogram(current_movie.duration, bin_range)
        current_i = np.where(current_hist == 1)[0][0]
        autotexts[current_i].set_color("white")

    return fig, ax


def plot_gender(df):
    fig, ax = plt.subplots()

    df.pipe(pps.assign_gender_ratio)
    gender_ratio = np.mean(df.gender_ratio)
    
    ax.pie([gender_ratio, 1-gender_ratio],
           labels=["female","male"],
           colors=["xkcd:dusty teal","xkcd:beige"],
           autopct="%1.1f%%",)

    return fig, ax


if __name__ == "__main__":
    df = pd.read_csv(ROOT_PATH / "results" / "oscars.csv")
    fig, ax = plot_duration(df)
    fig_dir = ROOT_PATH / "docs" / "assets"
    fig.savefig(fig_dir / "duration.png", bbox_inches="tight", dpi=200)

