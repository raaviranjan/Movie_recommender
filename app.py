# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


movie = pd.read_csv("bollywood_full_1950-2019.csv")

# def get_movie_db():
    # global movie
    # movie = pd.read_csv("bollywood_full_1950-2019.csv")
    # return movie

def set_movie_db(updated_movie_db):
    global movie
    movie = updated_movie_db
    
def get_updated_movie_db():
    return movie
    
def preprocessing():
    #movie = get_movie_db()
    movie = pd.read_csv("bollywood_full_1950-2019.csv")
    movie = movie.rename(columns={'original_title':'title'})
    movie.drop(['title_x','title_y','tagline','wins_nominations'],axis=1,inplace=True)
    movie['title'] = movie['title'].str.lower()
    movie.dropna(subset=['story','actors','imdb_rating','imdb_votes'],inplace=True)
    movie['poster_path'] = movie['poster_path'].fillna('https://www.csaff.org/wp-content/uploads/csaff-no-poster.jpg')
    movie['genres'] = movie['genres'].apply(lambda x:x.split('|'))
    movie['genres'] = movie['genres'].apply(lambda x:' '.join(x))
    movie['actors'] = movie['actors'].apply(lambda x:x.split('|'))
    movie['actors'] = movie['actors'].apply(lambda x:' '.join(x))
    movie['comb'] = movie['genres']+" "+movie['summary']+" "+movie['actors']
    set_movie_db(movie)

def recommend_movies(movie_name):
    movie = get_updated_movie_db()
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(movie['comb'])
    cosine_sim = cosine_similarity(count_matrix)
    if not movie[movie['title'] == movie_name].empty:
        index = movie[movie['title'] == movie_name].index.values[0]
        list_of_tuples = list(enumerate(cosine_sim[index]))
        movie_score_array = sorted(list_of_tuples, key = lambda x:x[1], reverse = True)
        #removing first movie as this is the movie searched by user , so[1:11]
        top_10_sim_movies = get_10_sim_movies_list(movie_score_array[1:11],movie)
        return top_10_sim_movies
    
    return 0
    
def get_10_sim_movies_list(movie_score_array,movie_db):
    movie_list = {}
    for row in movie_score_array:
        movie_list[movie_db['title'].iloc[row[0]]] = movie_db['poster_path'].iloc[row[0]]
    return movie_list

def get_movie_from_db(movie_name):
    movie = get_updated_movie_db()
    return movie[movie['title'] == movie_name.lower()]
    
@app.route('/')
def home():
    preprocessing()
    m = get_updated_movie_db()
    movie_title_list = m['title'].tolist()
    return render_template('index.html', flag = False, movie_title_list = movie_title_list)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_name = request.form['movie_name']
    movie_list = recommend_movies(movie_name.lower())
    
    m = get_updated_movie_db()
    movie_title_list = m['title'].tolist()
    
    if(movie_list):
        movie_row = get_movie_from_db(movie_name.lower())
        movie_title = movie_row.title.iloc[0]
        movie_poster = movie_row.poster_path.iloc[0]
        movie_overview = movie_row.summary.iloc[0]
        movie_rating = movie_row.imdb_rating.iloc[0]
        movie_votes = movie_row.imdb_votes.iloc[0]
        movie_genre = movie_row.genres.iloc[0]
        movie_release_date = movie_row.release_date.iloc[0]
        movie_runtime = movie_row.runtime.iloc[0]
        
        
        return render_template('index.html',movie_list = movie_list, title = movie_title.capitalize(), overview = movie_overview,
                                rating = movie_rating, vote_count = movie_votes, genres = movie_genre.replace(" ","|"), release_date = movie_release_date,
                                runtime = movie_runtime, poster = movie_poster, flag = False, movie_title_list = movie_title_list)

    return render_template('index.html',movie_list = movie_list, flag = True, movie_title_list = movie_title_list)

if __name__ == '__main__':
    app.run(debug=True)