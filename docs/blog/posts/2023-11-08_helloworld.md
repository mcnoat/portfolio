---
date: 2023-11-08
draft: false
---

# Hello world!

On this website I intend to build a bunch of visualizations of different collections of movies.
These collections could be winners of film festivals (e.g. [Cannes](https://en.wikipedia.org/wiki/Palme_d%27Or#Winners)), Sight and Sound's [Top 100](https://www.bfi.org.uk/sight-and-sound/greatest-films-all-time) or - but admittedly this is a bit of a pipe dream - any given list on [The Movie DB](https://www.themoviedb.org/).

<!-- more -->

I want to use this blog for documenting the updates to the movie dashboard project and publishing small data analyses I did for fun and/or for learning new skills.
I intend to announce the next features I want to add to the dashboard project on this blog in order to hold myself publicly accountable.
For now, let's keep things simple.
For "version 1.0" I want to accomplish the following things:

* create a database of Oscar Best Picture winners, pulled from WikiData
* create the following plots for the collection of winners:
    * pie chart of the movie durations (where the durations are grouped into categories of run times in 30 minutes increments)
    * pie chart of the movie director's genders

In the early versions, these charts are going to be simple images.
In the long term, I would like to turn them into interactive plots, using Plotly's  [Dash](https://plotly.com/dash/) package.
