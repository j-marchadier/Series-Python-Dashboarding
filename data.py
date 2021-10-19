import pandas as pd
import numpy as np
import os
import json


pd.options.mode.chained_assignment = None


######### Recuperation de la data base #####################
def download_data_set():
    print("Downloading data set ...")
    kaggle_data = {"username": "julienmarchadier", "key": "02de99c2fe1cf5aca1b01c1294e880dd"}
    os.environ['KAGGLE_USERNAME'] = kaggle_data["username"]
    os.environ['KAGGLE_KEY'] = kaggle_data["key"]
    import kaggle
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
                     dtype={"genre": str, "series_or_movies": "str"},
                     parse_dates=["release_date", "netflix_date"]
                     )
    print("Read .csv done.")
    return df



########## Data cleaning  ###########
def clean_dataframe(data):
    print("Cleaning data set ...")
    # Drop the $ character
    data["box_office"] = data["box_office"].str.replace("$", "", regex=True)
    data["box_office"] = data["box_office"].str.replace(",", "", regex=True)
    data["box_office"] = data["box_office"].dropna().astype('int')

    # Get only the year value in date
    data["release_date"] = data["release_date"].dt.year.dropna().astype('int32')
    data["netflix_date"] = data["netflix_date"].dt.year.dropna().astype('int32')
    data.rename(columns={"release_date": "release_year", "netflix_date": "netflix_year"}, inplace=True)
    
    #Modify col
    data["series_or_movies"] = data["series_or_movies"].str.replace("Movie","Movies",regex=True)


    return data


########### Spare Country_availability ###########
def split_country_availability(data):
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
def split_genre(data):
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
    a = pd.concat(dataframes, axis=1)
    return a.loc[:, ~a.columns.duplicated()]


def pivot_country_data(data_country_merge):
    data_country_merge.drop(["country_availability"], axis=1, inplace=True)
    # print(data_country_merge.columns)

    finale_country = data_country_merge.melt(
        id_vars=['title', 'genre', 'series_or_movies', 'hidden_gem_score', 'run_time',
                 'director', 'writer', 'imdb_score', 'awards_received',
                 'awards_nominated', 'box_office', 'release_year', 'netflix_year',
                 'summary', 'imdb_vote', 'poster'],
        value_vars=['Lithuania', 'Poland', 'France',
                    'Iceland', 'Italy', 'Spain', 'Greece', 'Czech Republic', 'Belgium',
                    'Portugal', 'Canada', 'Hungary', 'Mexico', 'Slovakia', 'Sweden',
                    'South Africa', 'Netherlands', 'Germany', 'Thailand', 'Turkey',
                    'Singapore', 'Romania', 'Argentina', 'Israel', 'Switzerland',
                    'Australia', 'United Kingdom', 'Brazil', 'Malaysia', 'India',
                    'Colombia', 'Hong Kong', 'Japan', 'South Korea', 'United States',
                    'Russia'],
        var_name='country',
        value_name="is_country")

    finale_country = finale_country[finale_country["is_country"] ==True].reset_index(drop=True)
    finale_country.drop(["is_country"],axis=1, inplace=True)

    finale_country.replace("South Korea","Korea, Republic of", inplace= True)
    finale_country.replace("Russia","Russian Federation", inplace= True)
    
    return finale_country


def main():
    download_data_set()
    df = read_csv()
    data = clean_dataframe(df)
    data_country_availability = split_country_availability(data)
    data_genre_availability = split_genre(data)
    data_country_merge = merge_data(data, data_country_availability)
    data_genre_merge = merge_data(data, data_genre_availability)

    #Return data 
    data.drop(["genre","country_availability"],axis=1, inplace=True)
    final_country = pivot_country_data(data_country_merge)
    final_genre = data_genre_merge


    print("Cleaning done.")
    return data ,final_country,final_genre

if __name__ == "__main__":
    main()