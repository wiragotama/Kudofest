import sqlalchemy as sa
import pandas as pd
import re
import numpy as np
import random
from pandas import DataFrame
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base


class GenreBasedRecommendation:
    dbName = "kudofest"
    hostname = "localhost"
    usr = "root"
    password = ""

    def __init__(self):
        engine_statement = "mysql+pymysql://" + self.usr + ":" + self.password + "@" + self.hostname + "/" + self.dbName
        self.engine= sa.create_engine(engine_statement,)
        self.user_behaviours = pd.read_sql("user_behaviours", self.engine).as_matrix()
        self.movies = pd.read_sql("movies", self.engine)
        print("Genre Ctor")
        return

    def update(self):
        self.user_behaviours = pd.read_sql("user_behaviours", self.engine).as_matrix()

    def topNGenre(self, userId):
        for user in self.user_behaviours:
            if(user[0] == userId):
                selectedUser = user

        #find top 5 genre
        top5 = [[1, selectedUser[1]]]
        min = selectedUser[1];
        for i in range(2,19):
            if(len(top5) < 5):
                popular = [i,selectedUser[i]]
                top5.append(popular)
                if(selectedUser[i] < min):
                    min = selectedUser[i]
            else:
                swapped =false
                j=0
                while(j<5 and swapped ==false):
                    if(top5[j][1] < selectedUser[i]):
                        swapped = true
                        min = selectedUser[i]
                        del top5[j]
                        top5.append([i,selectedUser[i]])
                    j+=1

        return top5

    def recommend(self, userId, viewed):
        genre = ["action","adventure","animation","childrens","comedy","crime","documentary","drama","fantasy","film_noir","horror","musical","mystery","romance","sci_fi","thriller","war","western"]
        top5 = GenreBasedRecommendation.topNGenre(self, userId)
        top15 = []
        for i in range(len(top5)):
            corresponding_genre = self.movies.query(genre[top5[i][0]-1] + "==1").as_matrix()
            # sort
            for x in range(len(corresponding_genre)):
                for y in range(x, len(corresponding_genre)):
                    if (corresponding_genre[x][21] > corresponding_genre[y][21]):
                        temp = corresponding_genre[x]
                        corresponding_genre[y] = corresponding_genre[x]
                        corresponding_genre[y] = temp
            # get best 3
            for i in range(3):
                if (corresponding_genre[i][0] not in top15) and (corresponding_genre[i][0] not in viewed):
                    top15.append(corresponding_genre[i][0])
        return top15

# main
# recommender = GenreBasedRecommendation()
# neighbors = recommender.recommend(1, [])
# print(neighbors)
