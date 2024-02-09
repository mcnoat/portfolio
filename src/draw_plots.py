#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 23:04:45 2022

@author: moritz
"""

# Python package index
import pandas as pd
import plotly.express as px

# custom scripts
import pipes as pps
from utils import ROOT_PATH


def plot_duration(df, ymin: int = 70, ymax: int = 240):

    most_recent_year = list(df.year_awarded)[-1]
    color_lst = ["red" if val == most_recent_year else "blue" for val in df["year_awarded"]]
    
    fig = px.box(df, y="duration",
                 range_y=[int(0.98*ymin), int(1.01*ymax)],
                 color=color_lst,
                 points="all",
                 boxmode="overlay",
                 hover_data=["title", "year_awarded"])

    fig.update_traces(selector=0, name="rest")
    fig.update_traces(selector=1, name=most_recent_year)
    fig.update_yaxes(title_text="duration [min]")
    fig.update_layout(width=300)

    return fig


def plot_gender(df):
    fig, ax = plt.subplots()

    df.pipe(pps.assign_gender_ratio)
    gender_ratio = np.mean(df.gender_ratio)

    ax.pie(
        [gender_ratio, 1 - gender_ratio],
        labels=["female", "male"],
        colors=["xkcd:dusty teal", "xkcd:beige"],
        autopct="%1.1f%%",
    )

    return fig, ax


if __name__ == "__main__":
    df = pd.read_csv(ROOT_PATH / "results" / "awards.csv")
    fig = plot_duration(df, "oscar")
    fig_dir = ROOT_PATH / "docs" / "assets"
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10))
    fig.write_image(fig_dir / "duration.png")
