import pandas as pd
import numpy as np
import os

kaggle_data = {"username": "julienmarchadier", "key": "02de99c2fe1cf5aca1b01c1294e880dd"}
os.environ['KAGGLE_USERNAME'] = kaggle_data["username"]
os.environ['KAGGLE_KEY'] = kaggle_data["key"]
import kaggle

pd.options.mode.chained_assignment = None

######### Recuperation de la data base #####################
# https://www.kaggle.com/ashishgup/netflix-rotten-tomatoes-metacritic-imdb
# kaggle.api.dataset_download_files('ashishgup/netflix-rotten-tomatoes-metacritic-imdb', path='.', unzip=True)
if os.path.exists("netflix-rotten-tomatoes-metacritic-imdb.zip"):
    os.remove("netflix-rotten-tomatoes-metacritic-imdb.zip")


########################

########## Import data ################
def read_csv():
    df = pd.read_csv('netflix-rotten-tomatoes-metacritic-imdb.csv',
                     skiprows=1,
                     names=["title", "genre", "tags", "languages", "series_or_movies", "hidden_gem_score",
                            "country_availability", "run_time", "director", "writer", "actors",
                            "view_rating", "imdb_score", "rotten_tomatoes_score", "metacritic_score",
                            "awards_received", "awards_nominated", "box_office", "release_date", "netflix_date",
                            "production_house", "netflix_link", "imdb_link", 'summary', "imdb_vote", "image",
                            "poster", "tmdb_trailer", "trailer_site"],
                     usecols=["title", "genre", "series_or_movies", "hidden_gem_score",
                              "country_availability", "run_time", "director", "writer", "imdb_score",
                              "awards_received", "awards_nominated", "box_office", "release_date", "netflix_date",
                              'summary', "imdb_vote",
                              "poster"],
                     dtype={"genre": str, "series_or_movies": "category"},
                     parse_dates=["release_date", "netflix_date"]
                     )
    return df


########## Data cleaning  ###########
def clean_dataframe(data):
    # Drop the $ character
    data["box_office"] = data["box_office"].str.replace("$", "", regex=True)

    # Get only the year value in date
    data["release_date"] = data["release_date"].dt.year
    data["netflix_date"] = data["netflix_date"].dt.year
    data.rename(columns={"release_date": "release_year", "netflix_date": "netflix_year"}, inplace=True)

    return data


########### Spare Country_availability ###########
def separe_country_availability(data):
    # fillna() <- replace les cases na
    # Creation dataset about country
    data_country_availability = data[["title", "release_year", "country_availability"]]
    data_country_availability["country_availability"] = data["country_availability"][
        ~data["country_availability"].isna()].map(lambda row: row.split(","))

    # Looking for all genre available
    all_country_availability = data_country_availability["country_availability"][
        data_country_availability["country_availability"].str.len() == 36].iloc[0]

    # creation of col for each countries find
    for country in all_country_availability:
        data_country_availability[country] = np.where(data["country_availability"].str.contains(country), True, False)

    data_country_availability.drop(["country_availability"], axis=1, inplace=True)
    return data_country_availability


########### Spare Genre ###########
def separe_genre(data):
    # Creation dataset about genre
    data_genre_availability = data[["title", "release_year", "genre"]]
    data_genre_availability["genre"] = data["genre"][~data["genre"].isna()].map(lambda row: row.split(", "))

    # Looking for all genre available
    all_genre_availability = []
    data_genre_availability["genre"][~data_genre_availability["genre"].isna()].map(
        lambda row: [all_genre_availability.append(genre1) for genre1 in row])
    all_genre_availability = np.unique(all_genre_availability)

    # Creation of col for each countries find
    for genre in all_genre_availability:
        data_genre_availability[genre] = np.where(data["genre"].str.contains(genre, na=False), True, False)

    data_genre_availability.drop(["genre"], axis=1, inplace=True)

    return data_genre_availability


########### Merge Dataframes ###########
def merge_data(*args):
    dataframes = []
    for n in args:
        dataframes.append(n)
    return pd.concat(dataframes, axis=1)


def main():
    df = read_csv()
    data = clean_dataframe(df)
    data_country_availability = separe_country_availability(data)
    data_genre_availability = separe_genre(data)
    data_final = merge_data(data, data_genre_availability, data_country_availability)

    return data_final
