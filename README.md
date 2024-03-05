# taylor_swift_discography
This repository contains an ongoing project to compile and analyze Taylor Swift's discography, including all songs she's written for other artists. All data, including lyrics, is scraped initially from [Genius](https://genius.com/) via [parsel](https://parsel.readthedocs.io/) and placed into a SQLite database. SQL queries transform the data via [pandas](https://pandas.pydata.org/) and [sqlite3](https://docs.python.org/3/library/sqlite3.html) before ultimately being visualized via [matplotlib](https://matplotlib.org/) and [seaborn](http://seaborn.pydata.org/index.html).

**Please note this project is a work-in-progress and not yet complete.**

## Directory
* **[data](./data)**: contains pickle versions of both raw and cleaned webscraping data, as well as SQLite database file
* **[figures](./figures)**: contains project pngs, including database schema (courtesy of [dbdiagram.io](https://dbdiagram.io))
  * **[charts](./figures/charts)**: contains all matplotlib/seaborn charts created
* **[notebooks](./notebooks)**: contains all Juptyter Notebooks
  * **[01_data_collection.ipynb](./notebooks/01_data_collection.ipynb)**: initial webscraping from Genius using parsel, creating dataframes and database of Taylor Swift songs and lyrics
  * **[02_collaborator_stats.ipynb](./notebooks/02_collaborator_stats.ipynb)**: exploratory data analysis of Taylor Swift's collaborations and most frequent collaborators
* **[fonts](./fonts)**: contains font `ttf` files used in charts (courtesy of [Google Fonts](https://fonts.google.com/))
* **[sql](./sql)**: contains all SQL queries used in project (note: they are written in SQLite SQL)
* **[src](./src)**: contains all Python modules used in project 

## Constraints and Limitations of Discography
This discography prioritizes *song* coverage over *album* coverage; this means that deluxe versions of albums with more songs are preferred over standard versions, and that album releases are preferred over single/EP releases. While not all versions of a song's release will be covered in this dataset, it contains every unique song. Rerecorded songs count as separate entries from their original versions.

Please see table below for more information on what is and isn't included in the discography:

| Included in Discography | Not Included in Discography |
| -- | -- |
| Songs released on Taylor Swift studio albums  | Duplicate song entries (e.g. for single release, album release, deluxe album release, etc.) |
| Songs released on Taylor Swift rerecorded "Taylor's Version" albums | Unreleased/leaked songs and demos |
| Songs by Taylor Swift for soundtracks or released as non-album singles | Covers of Taylor Swift songs by other artists |
| Remixes of Taylor Swift songs featuring new performing artists | Remixes/acoustic versions of songs not featuring new performing artists|
| Songs written by Taylor Swift for other artists, even if they don't feature Taylor | Live versions of songs/song mashups previously accounted for |
| Songs by other artists featuring Taylor Swift | Songs that sample/interpolate Taylor Swift songs, even if they list her as a writer or feature |
| Song covers by or featuring Taylor Swift that have been officially recorded and released | Songs that only exist in video format (DVD, live show recording, etc.) |
