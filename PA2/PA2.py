"""
Author: Samantha Gregoryk
Assignment: PA2
Class: CPTS 315
Section: 01
Date: October 19th, 2020
"""
import numpy as np
import pandas as pd
from itertools import combinations
from numpy import linalg
import scipy.spatial

k = 5

def user_profile(file):
    
    # create empty list
    L = {}
    
    # for each line in the ratings file
    for i in file:
        # csv file
        sep_line = i.split(',')
        
        # assign each item 
        userId = sep_line[0]
        movieId = sep_line[1]
        rating = sep_line[2]
        
        # create dictionary for userId
        # if user has no ratings...
        if L.get(userId) is None:
            # return an empty list
            L[userId] = {}
    
        # dictionary of the movie and the rating the user gave 
        # user = {'movieId':'rating'}
        else:
            L[userId][movieId] = rating
        
    # return user dictionary with 'moviesId' : 'rating'
    return L

def movie_profile(file):
    
    # create empty list
    M = {}

    # for each line in the ratings file
    for i in file:
        # csv file
        sep_line = i.split(',')

        # assign each item 
        movieId = sep_line[1]
        rating = sep_line[2]

        # create dictionary for MovieId
        # if movie has no ratings... 
        if M.get(movieId) is None:
            # return empty list
            M[movieId] = []
        
        # dictionary of the movie and the multiple ratings
        # movie = ['rating']
        else:
            M[movieId].append(rating)
    
    # return movie dictionary with 'rating'
    return M

def define_matrix(m):
   
    # create data frame first
    df = pd.DataFrame(list(m.values()), index = m.keys())
    
    # delete rows with all nan
    df = df.dropna(how = 'all')

    # create matrix from data frame
    matrix = np.asmatrix(df.values)
    
    # return matrix
    return matrix

# since we normalized the matrix, we can compute centered cosine 
# need to center the normalize first
def normalized_matrix(m):
    
    xmax = m.max()
    xmin = m.min()
    
    norm_matrix = (m - xmin)/(xmax - xmin)

    return norm_matrix
    
def similarity_scores(matrix): 
    
    # centred cosine computation for movie x to movie y
    
    # create empty list 
    S = {}
    
    # return r-length tuples in sorted order with 
    # no repeated elements at a length of 2
    combo = combinations([i for i in range(matrix.shape[1])], 2)

    for i in combo:
        
        # row:col
        x = matrix[:,i[0]]
        y = matrix[:,i[1]]
    
        # cosine 
        
        # dot -> sum((r1:c1 * r2:c1) + (r1:c2 * r2:c2) + ...)
        # linalg.norm -> sqrt(sum((r1:c1^2) + (r1:c2^2) + ...))
        S[i] = np.dot(x, y) / ((linalg.norm(x)) * (linalg.norm(y)))

    # return L
    return S

def neighborhood_selection(arr, k):
    
    # [1,2,3,4,5]
    k_lst = list(range(k + 1))[1:] 
    
    # create empty list
    N = []

    # for each row in the array
    for row in arr:
        # each item is in a row
        data = np.vstack(row)
        
        # kd-tree
        tree = scipy.spatial.cKDTree(data)
        
        # find k nearest neighbors for each element of data, 
        # squeezing out the zero result
        dd, ii = tree.query(data, k = k_lst)
        
        # apply an index filter on data to get the nearest 
        # neighbor elements
        closest = data[ii].reshape(-1, k)
        
        # append each row 
        N.append(closest)
    
    # return matrix of top 5 nearest neighbors
    return np.stack(N)
    
def estimate_ratings(movie1, movie2):
    return
    
def recommended_movies(movies):
    return 

# read in ratings.csv
with open('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA2/movie-lens-data/ratings.csv', "r") as f1:
    # returns a list containing each line in the file as a list item
    ratings_file = f1.readlines()
    
print("Constructing User Profiles And Their Movie + Ratings...")
user_rating = user_profile(ratings_file)

print("Constructing Movie Profiles And Their Ratings...")
movie_rating = movie_profile(ratings_file)

print("Creating Movie Matrix...")
movie_matrix = define_matrix(movie_rating).astype(float)

# mask nan values
new_matrix = np.ma.array(movie_matrix, mask = np.isnan(movie_matrix))

print("Creating Normalized (Centered) Matrix...")
norm_matrix1 = normalized_matrix(new_matrix)

# change masked matrix back 
norm_matrix2 = np.squeeze(np.asarray(norm_matrix1))

# change nan to 0
norm_matrix2[np.isnan(norm_matrix2)] = 0

print("Creating Similarity Scores From Centered Matrix...")
scores = similarity_scores(norm_matrix2)

score_df = pd.DataFrame(scores, index = [0])
score_arr = np.array(score_df)

print("Computing The Nearest Neighbor (N = 5) For Each Movie...")
# five similarity scores for each movie in matrix
nearest_neighbors = neighborhood_selection(score_arr, k)

# go through the same process to find the nearest neighbor for users
z1 = define_matrix(user_rating).astype(float)
z2 = np.ma.array(z1, mask = np.isnan(z1))
z3 = normalized_matrix(z2)
z4 = np.squeeze(np.asarray(z3))
z4[np.isnan(z4)] = 0
z5 = similarity_scores(z4)
z6 = pd.DataFrame(z5, index = [0])
z7 = np.array(z6)

# returns matrix of top 5 nearest neighbors for each user comparison
user_nn = neighborhood_selection(z7, k)

print("Estimating The Ratings Of Other Users Who Didn’t Rate That Movie...")
est_ratings = estimate_ratings()

print("Computing The Recommended Movies For Each User...")
rec_movies = recommended_movies()

print("Top 5 Recommended Movies For Each User Saved In output.txt...")

with open('C:/Users/Samgr/OneDrive/Desktop/CPTS315/Homework/PA2/output.txt', "w") as w:
    
    # Output A in .txt
    w.write("OUTPUT \n")
        
    # output: <user> <movie1> <movie2> <movie3> <movie4> <movie5>
    for r in rec_movies:
        w.write(r , ' ' , r[0], ' ' , r[1], ' ' , r[2], ' ' , r[3], ' ' , r[4], '\n') 


