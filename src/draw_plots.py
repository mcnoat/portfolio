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
from src.utils import ROOT_PATH


def plot_duration(df):
    fig, ax = plt.subplots()

    hist, bin_edges = np.histogram(df.duration, [1, 90, 120, 150, 180])

    current_movie = df.tail(1)
    current_hist, _ = np.histogram(current_movie.duration, [1, 90, 120, 150, 180])
    current_i = np.where(current_hist == 1)[0][0]

    labels = ["$\leq 90$ min", "$\leq 120$ min", "$\leq 150$ min", "$\leq 180$ min"]
    cmap = sns.color_palette("deep")
    patches, texts, autotexts = ax.pie(
        hist,
        labels=labels,
        counterclock=False,
        startangle=90,
        autopct="%1.1f%%",
        colors=cmap,
    )
    autotexts[current_i].set_color("white")

    return fig, ax


if __name__ == "__main__":
    df = pd.read_csv("movie_data.csv")
    fig, ax = plot_duration(df)
    fig_dir = ROOT_PATH / "docs" / "assets"
    fig.savefig(fig_dir / "duration.png", bbox_inches="tight", dpi=200)
