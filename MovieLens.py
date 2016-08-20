import pandas as pd
from scipy.sparse import csc_matrix
import numpy as np
from sklearn.decomposition import TruncatedSVD

"""
Get Dataframes function: We load data from local files via pandas, merge them and create a pivot table for
SVD. We initialize TruncatedSVD to transform the data for later movie recommendations and return the transformed ratings and
movie list
"""
def getDataframes():
    #get data from csv
    ratings = pd.read_csv("ml-latest-small/ratings.csv",sep=",",names=["user_id","movie_id","rating","timestamp"])
    movies = pd.read_csv("ml-latest-small/movies.csv", sep=",",header=None,names=["movie_id","title","genre"])
     #drop first row of the 2 dataframes
    ratings.drop(ratings.index[0], inplace=True)
    movies.drop(movies.index[0], inplace=True)

    #create pivot table from the 2 dataframes and unite them
    MovieLens = pd.merge(movies,ratings)
    ratings_movie_dataframe = MovieLens.pivot_table(values="rating", columns="title", index="user_id",aggfunc=np.sum,fill_value=0)
    movie_index = ratings_movie_dataframe.columns



     #create variables for average rating
    rating_list = list()

    counter = 0
    for line in ratings_movie_dataframe.values.T:
        rating = 0
        rating_counter = 0
        for i in range(0, len(line)):
            try:
                line[i] = float(line[i])
                if line[i] > 0:
                    rating += line[i]
                    rating_counter += 1
            except:
                ratings_movie_dataframe.values.T[counter][i] = 0

        rating_list.append(rating/rating_counter)
        counter += 1

    #init SVD and transform rating data to matrices
    svd = TruncatedSVD(n_components=10, random_state=101)
    svd_matrix = svd.fit_transform(ratings_movie_dataframe.values.T)


    return (svd_matrix, movie_index,rating_list)
