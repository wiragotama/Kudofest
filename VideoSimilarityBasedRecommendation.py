import sqlalchemy as sa
import pandas as pd
import numpy as np
import math
import random
from pandas import DataFrame
from sqlalchemy import *

class VideoBasedRecommendation:
    dbName = "kudofest"
    hostname = "localhost"
    usr = "root"
    password = ""

    def __init__(self):
        """
        Default constructor, load the neccesary data

        :return:
        """
        engine_statement = "mysql+pymysql://" + self.usr + ":" + self.password + "@" + self.hostname + "/" + self.dbName
        self.engine= sa.create_engine(engine_statement,)
        return

    def get_viewed_items(self, userId):
        """
        Getter

        :return: array of id(s) of viewed items
        """
        return pd.read_sql("ratings", self.engine).query("id_user == " + str(userId)).as_matrix()

    def recommend(self, userId):
        """
        Recommend movies for input (userId), with constraint viewed items

        :return: array of id(s) of recommended movies.
        """
        viewed = pd.read_sql("ratings", self.engine).query("id_user == " + str(userId)).as_matrix()
        # sort
        for i in range(len(viewed)):
            for j in range(i, len(viewed)):
                if (viewed[j][2] > viewed[i][2]):
                    temp = viewed[j]
                    viewed[j] = viewed[i]
                    viewed[i] = temp

        # select the best score
        candidate = []
        i = 0;
        prev = viewed[0][2]
        while (i < len(viewed)):
            if (prev != viewed[i][2]):
                break
            candidate.append(viewed[i][1])
            prev = viewed[i][2]
            i += 1
        random.shuffle(candidate)
        return VideoBasedRecommendation.__get_neighbor_movie__(self, candidate[0])

    def __check_similarity__(self, movie1, movie2):
        """
        Check similarity rate between 2 movies

        :return: array of movies id(s)
        """
        sim = 0
        for i in range (3, 21):
            if (movie1[i] == movie2[i]):
                sim +=1
        return sim

    def __get_neighbor_movie__(self, candidate_id):
        """
        Get the most similar movie with respect to candidate_id

        :return: array of movies id(s)
        """
        current_movie = pd.read_sql("movies", self.engine).query("id_movie == " + str(candidate_id)).as_matrix()
        movies = pd.read_sql("movies", self.engine).as_matrix()
        candidate = []
        for i in range(len(movies)):
            simRate = VideoBasedRecommendation.__check_similarity__(self, current_movie[0], movies[i])
            candidate.append([movies[i][0], simRate]) #id movie

        # sort
        for i in range(len(candidate)):
            for j in range(i, len(candidate)):
                if (candidate[j][1] > candidate[i][1]):
                    temp = candidate[j]
                    candidate[j] = candidate[i]
                    candidate[i] = temp

        # select the best score
        out = []
        i = 0;
        prev = candidate[0][1]
        while (i < len(candidate)):
            if (prev != candidate[i][1]):
                break
            out.append(candidate[i][0])
            prev = candidate[i][1]
            i += 1
        random.shuffle(out)
        return out[0:5]


# Main program
recommender = VideoBasedRecommendation()
neighbors = recommender.recommend(20)
print(neighbors)
