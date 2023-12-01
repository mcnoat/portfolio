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

    step_size = 30
    min_duration = int(df.duration.min())
    lower_bound = (min_duration // step_size + 1) * step_size
    max_duration = int(df.duration.max())
    upper_bound = (max_duration // step_size + 1) * step_size
    bin_range = [1] + list(range(lower_bound, upper_bound + 1, step_size))

    hist, bin_edges = np.histogram(df.duration, bin_range)

    labels = [f"$\\leq {duration}$ min" for duration in bin_range[1:]]
    cmap = sns.color_palette("deep")
    patches, texts, autotexts = ax.pie(
        hist,
        labels=labels,
        counterclock=False,
        startangle=90,
        autopct="%1.1f%%",
        colors=cmap,
    )

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
           colors=["xkcd:dusty teal","xkcd:beige"])

    return fig, ax


if __name__ == "__main__":
    df = pd.read_csv(ROOT_PATH / "results" / "oscars.csv")
    fig, ax = plot_gender(df)
    fig_dir = ROOT_PATH / "docs" / "assets"
    fig.savefig(fig_dir / "genders.png", bbox_inches="tight", dpi=200)

