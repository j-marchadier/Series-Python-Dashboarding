import pandas as pd
import numpy as np

#https://www.kaggle.com/amritvirsinghx/web-series-ultimate-edition
df = pd.read_csv('All_Streaming_Shows.csv',
                skiprows=1,
                names=["title","year","content_rating","imdb_rating","r_rating","genre","description","nb_seasons","streaming_platform"],
                dtype={"title": str,
                    "Year Released" : int,
                    "IMDB Rating" : float,
                    "R Rating" : int,
                    "Genre" : str,
                    "Description" : str,
                    "nb_seasons" : str,
                    "Streaming Platform" : str})
print(df.nb_seasons.str.replace("Seasons", "").str.replace("Season", ""))
#print(df.nb_seasons)
#print(df.info())