import streamlit as st
import pandas as pd
import pickle


# Streamlit setup
st.set_page_config(
    page_title="Cine Magic - File",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

# Load movies data from pickle file
movies_dict = pickle.load(open('movie-files/movie_dict.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)
similarity = pickle.load(open('movie-files/similarity.pkl', 'rb'))

st.header("Movies list")
st.write(movies_df)

with open('movie-files/Best_movies.pkl', 'rb') as f:
    Popular_movies = pickle.load(f)

st.header("Popular Movie List")
st.write(Popular_movies)

with open('movie-files/genres_movie_list.pkl', 'rb') as f:
    Movies = pickle.load(f)

Movies = Movies.sort_values('rating', ascending=False)

st.header("Movie List For Genre")
st.write(Movies)
