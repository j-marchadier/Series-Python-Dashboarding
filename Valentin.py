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

data["genre"][~data["genre"].isna()] = data["genre"][~data["genre"].isna()].map(lambda row : row.split(","))
#fillna() <- remplacer les cases na
#print((data["genre"]))
print(data["genre"][0])
#print(data["genre"][0].split(","))
print(len(data["genre"][0]))
print (max(data["genre"].str.len())) 
newlist=[]
for i in range (10):
    for j in range(len(data["genre"][i])):
        newlist.append(data["genre"][i][j])
        #print(np.unique(data["genre"][i][j]))
print(np.unique(newlist))
#print(np.unique(data["genre"][0].split(","))[0])
###Retrouver liste d'uniques###
###Sous table avec column == chaque genre###
###  For i genre, si dans la ligne genre il y a le genre, alors true sinon false ###
