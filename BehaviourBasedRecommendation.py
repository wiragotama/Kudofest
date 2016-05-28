import sqlalchemy as sa
import pandas as pd
import numpy as np
import math
import random
from pandas import DataFrame
from sqlalchemy import *

class BehaviourBasedRecommendation:
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
        self.user_behaviours = pd.read_sql("user_behaviours", self.engine).as_matrix()
        self.ratings = pd.read_sql("ratings", self.engine)
        return

    def recommend(self, userId, viewed):
        """
        Recommend movies for input (userId), with constraint viewed items

        :return: array of id(s) of recommended movies.
        """
        K = 5
        neighbors = BehaviourBasedRecommendation.__neighbor_scoring__(self, userId)

        # sort neighbor scores
        for i in range(len(neighbors)):
            for j in range(i, len(neighbors)):
                if (neighbors[j][1] > neighbors[i][1]):
                    temp = neighbors[j]
                    neighbors[j] = neighbors[i]
                    neighbors[i] = temp

        # get K nearest neighbor
        out = []
        for i in range(0, K):
            out.append(neighbors[i][0])
        return BehaviourBasedRecommendation.get_neighbor_movie(self, out, viewed)

    def __neighbor_scoring__(self, userId):
        """
        Score similarity of each users with input (userId)

        :return: Array of scores, each element consist of [neighbor_user_id, score]
        """
        for elmt in self.user_behaviours:
            if (elmt[0] == userId):
                selected = elmt
        selected = BehaviourBasedRecommendation.__normalize__(self, selected) # normalize value

        # neighbor_score
        neighbor = []
        i = 1;
        for curr_user in self.user_behaviours:
            if (not (selected[0] == curr_user[0])):
                curr_user_normalized = BehaviourBasedRecommendation.__normalize__(self, curr_user) #normalize value
                similarity = BehaviourBasedRecommendation.__check_similarity__(self, selected, curr_user_normalized)
                neighbor.append([i, similarity])
            else:
                neighbor.append([i, 0])
            i += 1
        return neighbor

    def __check_similarity__(self, user1, user2):
        """
        Similarity rate between 2 users behaviour

        :return: similarity rate
        """
        SC = 0.0
        divisor1 = 0.0
        divisor2 = 0.0
        for i in range(len(user1)):
            SC += user1[i] * user2[i]
            divisor1 += user1[i] * user1[i]
            divisor2 += user2[i] * user2[i]
        divisor = (math.sqrt(divisor1) * math.sqrt(divisor2))
        if (divisor==0.0):
            return 0.0
        else:
            return SC / divisor

    def __normalize__(self, behaviour):
        """
        Normalize data

        :return: normalized data
        """
        behaviour = np.delete(behaviour, [0])
        user_behaviour_float = []
        total = 0
        for i in range(len(behaviour)):
            total += behaviour[i]
        for i in range(len(behaviour)):
            if (total == 0):
                user_behaviour_float.append(0.0)
            else:
                user_behaviour_float.append( float(behaviour[i]) / float(total) )
        return user_behaviour_float

    def get_neighbor_movie(self, neighbors, viewed):
        """
        Get watched movies of K nearest neighbors

        :return: array of movies id(s)
        """
        movies_id = []
        for i in range(len(neighbors)):
            query_expression = "id_user == " + str(neighbors[i])
            rated_movies = self.ratings.query(query_expression).as_matrix()
            for j in range(len(rated_movies)):
                # print(rated_movies[j][1])
                if (not (rated_movies[j][1] in movies_id) and not (rated_movies[j][1] in viewed)):
                    movies_id.append(rated_movies[j][1])
        random.shuffle(movies_id)
        return movies_id[0:10]


# Main program
recommender = BehaviourBasedRecommendation()
neighbors = recommender.recommend(20, [])
print(neighbors)
