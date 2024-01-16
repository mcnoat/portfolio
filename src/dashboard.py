#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 18:39:23 2024

@author: moritz
"""

# Python packaging index
from dash import Dash, dcc, html
import pandas as pd

# custom scripts
import src.draw_plots as draw


# %% data preparataion

df = pd.read_csv("../results/oscars.csv")
fig = draw.plot_duration(df)


# %% app layout

stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(__name__, external_stylesheets=stylesheets)

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
                    id="dropdown-award",
                    options=[
                        {"label": "Academy Awards", "value": "oscar"},
                        {"label": "Palme d'Or", "value": "cannes"},
                    ],
                ),
            ),
        ),
    ]
)

# %% main

if __name__ == "__main__":
    app.run_server(debug=True)
