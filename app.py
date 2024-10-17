import streamlit as st
import pickle
import pandas as pd
import requests
''' This is a movie recommender system. You will get all the movies.'''

def fetch_poster(movie_id):
    """Fetch poster image URL using the TMDB API."""
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=dbe1069102f148caa614d0711641b8c0&language=en-US',
            timeout=5
        )
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', "")
    except Exception as e:
        print(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Poster+Unavailable"

def recommend(movie):
    """Recommend 5 movies similar to the selected movie."""
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['movie_id']
        recommended_movies.append(movies.iloc[i[0]]['title'])
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

# Load the movie data
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

# Ensure 'movie_id' column exists
if 'movie_id' not in movies.columns:
    movies['movie_id'] = movies.index

# Load similarity data
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit App Interface
st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie to get recommendations:",
    movies['title'].values
)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Display recommendations in columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
