import sqlalchemy as sa
import pandas as pd
import numpy as np
import random
import copy
from pandas import DataFrame
from sqlalchemy import *
from VideoSimilarityBasedRecommendation import VideoBasedRecommendation

class ProfileBasedRecommendation:
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
        self.users = pd.read_sql("users_profiles", self.engine).as_matrix()
        self.ratings = pd.read_sql("ratings", self.engine)
        print("Profile Ctor")
        return

    def update(self):
        self.users = pd.read_sql("users_profiles", self.engine).as_matrix()

    def quick_sort(self, left, right, candidate):
        left_row = left;
        right_row = right;
        pivot = candidate[(left_row + right_row) // 2][1]

        while left_row <= right_row:
            while (candidate[left_row][1] > pivot):
                left_row += 1
            while (candidate[right_row][1] < pivot):
                right_row -= 1
            if (left_row <= right_row):
                temp = candidate[left_row]
                candidate[left_row] = candidate[right_row]
                candidate[right_row] = temp
                left_row += 1
                right_row -= 1
        # endwhile
        if (left_row < right):
            ProfileBasedRecommendation.quick_sort(self, left_row, right, candidate)
        if (left < right_row):
            ProfileBasedRecommendation.quick_sort(self, left, right_row, candidate)

    def __neighbor_scoring__(self, userId):
        """
        Score similarity of each users with input (userId)

        :return: Array of scores, each element consist of [neighbor_user_id, score]
        """
        for elmt in self.users:
            if (elmt[0] == userId):
                selected = elmt

        # neighbor_score
        neighbors = []
        i = 1;
        for curr_user in self.users:
            if (not (selected[0] == curr_user[0])):
                similarity = ProfileBasedRecommendation.__check_similarity__(self, selected, curr_user)
                neighbors.append([i, similarity])
            else:
                neighbors.append([i, 0])
            i += 1
        return neighbors

    def recommend(self, userId, viewed):
        """
        Recommend movies for input (userId), with constraint viewed items

        :return: array of id(s) of recommended movies.
        """
        K = 5
        neighbors = ProfileBasedRecommendation.__neighbor_scoring__(self, userId)

        #sort
        ProfileBasedRecommendation.quick_sort(self, 0, len(neighbors)-1, neighbors)
        # print("Sorted")

        candidate = []
        i = 0;
        prev = neighbors[0][1]
        while (i < len(neighbors)):
            if (prev != neighbors[i][1]):
                break
            candidate.append(neighbors[i][0])
            prev = neighbors[i][1]
            i+=1
        random.shuffle(candidate)
        # print("Shuffled")

        # get K nearest neighbor
        out = []
        for i in range (0, min(K, len(candidate))):
            out.append(candidate[i])
        # print("Candidate")
        return ProfileBasedRecommendation.get_neighbor_movie(self, out, viewed)

    def __check_similarity__(self, user1, user2):
        """
        Similarity rate between 2 users profile

        :return: similarity rate
        """
        sim = 0
        for i in range (1,4):
            if (user1[i] == user2[i]):
                sim += 1
        return sim

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
                if (not (rated_movies[j][1] in movies_id) and not(rated_movies[j][1] in viewed)):
                    movies_id.append(rated_movies[j][1])
        random.shuffle(movies_id)
        # print("Neighbor")
        return movies_id[0:10]

# Main program
# viewed = VideoBasedRecommendation.get_viewed_items(25)
# recommender = ProfileBasedRecommendation()
# neighbors = recommender.recommend(25, [])
# print(neighbors)
