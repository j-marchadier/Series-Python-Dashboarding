import pandas as pd
import numpy as np

########## Import data ################
df = pd.read_csv('Web_series_data.csv',
                skiprows=1,
                names=["title","genre","tags","languages","series_or_movies","hidden_gem_score",
                            "country_availability","run_time","director","writer","actors",
                            "view_rating","imdb_scrore","rotten_tomatoes_score","metacritic_score",
                            "awards_received","awards_nominated","box_office","release_date","netflix_date",
                            "production_house","netflix_link","imdb_link",'summary',"imdb_vote","image",
                            "poster","tmdb_trailer","trailer_site"],
                dtype={"genre": str},
                parse_dates =["release_date","netflix_date"]
)

########## Data processing ###########
#Delete culunms
data = df.drop(["tags","languages","actors","view_rating","rotten_tomatoes_score","metacritic_score","production_house","netflix_link","imdb_link","tmdb_trailer","trailer_site","image"],axis =1)

#Drop the $ character
data["box_office"] = data["box_office"].str.replace("$","", regex=True)

#Get only the year value in date 
data["release_date"] = data["release_date"].dt.year
data["netflix_date"] = data["netflix_date"].dt.year
data.rename(columns={"release_date" : "release_year", "netflix_date" : "netflix_year"},inplace=True)

########### Separe Genre ###########

data_genre_availability= data[["title","release_year","genre"]]
data_genre_availability["genre"] = data["genre"][~data["genre"].isna()].map(
    lambda row : row.split(", "))    
vecteur_genre=[]
data_genre_without_nan=data["genre"].isna()

###Retrouver liste d'uniques###
for i in range (len(data_genre_availability["genre"])):
    if not(data_genre_without_nan[i]):
        for j in range(len(data_genre_availability["genre"][i])):
            vecteur_genre.append(data_genre_availability["genre"][i][j])

vecteur_genre=np.unique(vecteur_genre)

###Sous table avec column == chaque genre###
data_genre_no_Nan=data["genre"]
data_genre_no_Nan["genre"]=data_genre_no_Nan.fillna('')
#print(data_genre_no_Nan["genre"])
#print(data["genre"])
for genre in vecteur_genre :
    data_genre_availability[genre] = np.where(data_genre_no_Nan["genre"].str.contains(genre), True, False)

data_genre_availability.drop(["genre"],axis =1,inplace=True)
print(data_genre_availability["Comedy"][15475])
print(data_genre_availability)

