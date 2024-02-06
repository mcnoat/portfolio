#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 18:39:23 2024

@author: moritz
"""

# standard library
from typing import Literal

# Python packaging index
from dash import Dash, dcc, html, Input, Output
import pandas as pd

# custom scripts
import draw_plots as draw
import utils


def load_award_df(award: Literal["bear", "lion", "oscar", "palm"]):
    return pd.read_csv(f"../results/{award}.csv")


# %% data preparataion

df = pd.read_csv("../results/oscar.csv")
fig = draw.plot_duration(df)

dropdown_options = []
awards_dict = utils.load_json("awards.json")
for key, value in awards_dict.items():
    dropdown_dict = {}
    dropdown_dict["label"] = awards_dict[key]["name"]
    dropdown_dict["value"] = key
    dropdown_options.append(dropdown_dict)


# %% app layout

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)
server = app.server

app.layout = html.Div(
    [
        html.Div(
            className="row",
            children=html.H1(
                "Durations of film award winners", style={"textAlign": "center"}
            ),
        ),
        html.Div(
            className="row",
            children=html.Div(
                className="three columns",
                children=dcc.Graph(id="boxplot", figure=fig),
            ),
        ),
        html.Div(
            className="row",
            children=html.Div(
                className="three columns",
                children=dcc.Dropdown(
                    id="dropdown-award", options=dropdown_options, value="bear"
                ),
            ),
        ),
    ]
)

# %% callbacks


@app.callback(
    Output(component_id="boxplot", component_property="figure"),
    [Input(component_id="dropdown-award", component_property="value")],
)
def update_graph(chosen_value):
    if len(chosen_value) == 0:
        return {}
    else:
        df = load_award_df(chosen_value)
        fig = draw.plot_duration(df)
        return fig


# %% main

if __name__ == "__main__":
    app.run_server(debug=True)
