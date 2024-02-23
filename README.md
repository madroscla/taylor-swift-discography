# taylor_swift_discography
This repository contains an ongoing project to compile and analyze Taylor Swift's discography, including all songs she's written for other artists. All data, including lyrics, is scraped initially from [Genius](https://genius.com/) via [parsel](https://parsel.readthedocs.io/) and placed into a SQLite database. SQL queries transform the data via [pandas](https://pandas.pydata.org/) and [sqlite3](https://docs.python.org/3/library/sqlite3.html) before ultimately being visualized via [matplotlib](https://matplotlib.org/) and [seaborn](http://seaborn.pydata.org/index.html).

## Directory

* **[data](./data)**: contains pickle versions of both raw and cleaned webscraping data, as well as SQLite database file
* **[figures](./figures)**: contains project pngs, including database schema (courtesy of [dbdiagram.io](https://dbdiagram.io))
  * **[charts](./figures/charts)**: contains all matplotlib/seaborn charts created
* **[sql](./sql)**: contains all SQL queries used in project (note: they are written to run in SQLite); number in file name corresponds to connected notebook
* **[src](./src)**: contains all Python modules used in project; number in file name corresponds to connected notebook
* **[01_data_collection.ipynb](./01_data_collection.ipynb)**: initial webscraping from Genius using parsel, creating dataframes and database of Taylor Swift songs and lyrics
* **[02_discography_stats.ipynb](./02_discography_stats.ipynb)**: preliminary analysis of Taylor Swift's discography, including albums, collaborators, Genius song tags, etc.