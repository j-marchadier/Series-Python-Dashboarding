import pandas as pd
import numpy as np
import kaggle

pd.options.mode.chained_assignment = None

######### Recuperation de la data base #####################
#https://www.kaggle.com/ashishgup/netflix-rotten-tomatoes-metacritic-imdb
#kaggle.api.authenticate()
#kaggle.api.dataset_download_files('ashishgup/netflix-rotten-tomatoes-metacritic-imdb', path='.', unzip=True)
########################



########## Import data ################
def read_csv():
    df = pd.read_csv('netflix-rotten-tomatoes-metacritic-imdb.csv',
                    skiprows=1,
                    names=["title","genre","tags","languages","series_or_movies","hidden_gem_score",
                                "country_availability","run_time","director","writer","actors",
                                "view_rating","imdb_scrore","rotten_tomatoes_score","metacritic_score",
                                "awards_received","awards_nominated","box_office","release_date","netflix_date",
                                "production_house","netflix_link","imdb_link",'summary',"imdb_vote","image",
                                "poster","tmdb_trailer","trailer_site"],
                    usecols=["title","genre","series_or_movies","hidden_gem_score",
                                "country_availability","run_time","director","writer","imdb_scrore",
                                "awards_received","awards_nominated","box_office","release_date","netflix_date",
                                'summary',"imdb_vote",
                                "poster"],
                    dtype={"genre": str, "series_or_movies" : "category"},
                    parse_dates =["release_date","netflix_date"]
    )
    return df

########## Data cleanning  ###########
def clean_dataframe(data) :
    #Drop the $ character
    data["box_office"] = data["box_office"].str.replace("$","", regex=True)

    #Get only the year value in date 
    data["release_date"] = data["release_date"].dt.year
    data["netflix_date"] = data["netflix_date"].dt.year
    data.rename(columns={"release_date" : "release_year", "netflix_date" : "netflix_year"},inplace=True)

    return data

########### Separe Country_availability ###########
def separe_country_availability(data) :
    #fillna() <- remplacer les cases na
    #Création dataset about country
    data_country_availability = data[["title","release_year","country_availability"]]
    data_country_availability["country_availability"] = data["country_availability"][~data["country_availability"].isna()].map(lambda row : row.split(","))

    #Looking for all genre available
    all_country_availability =data_country_availability["country_availability"][data_country_availability["country_availability"].str.len() ==36].iloc[0]

    #création of col for each countries find
    for country in all_country_availability :
        data_country_availability[country] = np.where(data["country_availability"].str.contains(country), True, False)

    data_country_availability.drop(["country_availability"],axis =1,inplace=True)
    return data_country_availability

########### Separe Genre ###########
def separe_genre(data) :
    #Création dataset about genre
    data_genre_availability= data[["title","release_year","genre"]]
    data_genre_availability["genre"] = data["genre"][~data["genre"].isna()].map( lambda row : row.split(", "))    

    #Looking for all genre available
    all_genre_availability= []
    data_genre_availability["genre"][~data_genre_availability["genre"].isna()].map( 
        lambda  row : [all_genre_availability.append(genre1) for genre1 in row])
    all_genre_availability=np.unique(all_genre_availability)

    #Création of col for each countries find
    for genre in all_genre_availability :
        data_genre_availability[genre] = np.where(data["genre"].str.contains(genre,na=False), True, False)

    data_genre_availability.drop(["genre"],axis =1,inplace=True)

    return data_genre_availability



def main():
    df = read_csv()
    data = clean_dataframe(df) 
    data_country_availability = separe_country_availability(data)
    data_genre_availability = separe_genre(data)
    print(data_genre_availability)

    



    
if __name__ =="__main__":
    main()