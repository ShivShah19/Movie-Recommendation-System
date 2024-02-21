import streamlit as st
import pandas as pd
import pickle
import requests

# # Streamlit setup
st.set_page_config(
    page_title="Cine Magic",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
    
)

# Load movies data from pickle file
movies_dict = pickle.load(open('movie-files/movie_dict.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)
similarity = pickle.load(open('movie-files/similarity.pkl', 'rb'))

# Function to fetch movie poster
def fetch_Poster(id):
    try:
        url = 'https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US'.format(id)
        response = requests.get(url)
        data = response.json()

        if 'poster_path' in data:
            poster_path = data['poster_path']
            poster_link = "https://image.tmdb.org/t/p/w500/" + poster_path
            return poster_link
        else:
            print("Error: 'poster_path' not found in API response.")
            return None
    except Exception as e:
        print(f"An error occurred in fetching poster: {str(e)}")
        st.error(f"An error occurred in fetching poster: {str(e)}")
        return None

# Function to fetch movie and video links
def fetch_links(id):
    try:
        url = 'https://api.themoviedb.org/3/movie/{}/videos?api_key=c7ec19ffdd3279641fb606d19ceb9bb1'.format(id)
        response = requests.get(url)
        link_data = response.json()

        if 'results' in link_data and link_data['results']:
            link = link_data['results'][0].get('key', '')
            return link
        else:
            print("Error: No video link found in API response.")
            return None
    except Exception as e:
        print(f"An error occurred in fetching links: {str(e)}")
        st.error(f"An error occurred in fetching links: {str(e)}")
        return None

# Function to get Recommended movies
def getRecommendation(movie, range):
    index = movies_df[movies_df['title'] == movie].index[0]
    movie_list = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_movies_poster = []
    links = []
    id = []

    for i in movie_list[0:range]:
        movie_id = movies_df.iloc[i[0]].id
        recommended_movies.append(movies_df.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_Poster(movie_id))
        links.append(fetch_links(movie_id))
        id.append(movie_id)

    return recommended_movies, recommended_movies_poster, links, id


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit layout
with st.container(border=True):
    st.title(":red[*C*]ine:red[*M*]agic")
    st.subheader("Thousands of movies to discover. Want to Explore ? :red[Go For It ... 🚀]")

with st.container():
    Selected_movies = st.selectbox("**Explore the movies 📽️**", movies_df['title'].values, index=None, placeholder="Select or Search Your Movie...",)
    limit = st.slider('Range', 1, 50, 10)
    recomm = st.button("Recommendation")
    
    if recomm:
        try:
            if not Selected_movies:
                st.error('Please select or search a movie before clicking "Recommendation"', icon="🚨")
            else:
                titles, posters, links, id = getRecommendation(Selected_movies, limit)
                num_columns = 5
                columns = st.columns(num_columns)

                for i in range(len(titles)):
                    with columns[i % num_columns]:
                        image_link = st.image(posters[i])
                        link = titles[i]
                        if links[i]:
                            titles[i] = titles[i].replace(" ", "-").replace(".", "-").replace(":", "").lower()
                            home = "https://www.themoviedb.org/movie/{}-{}".format(id[i], titles[i])
                            
                            st.write(f"[{link}]({home})")

                            new_page_url = 'https://www.youtube.com/watch?v={}'.format(links[i])
                            st.link_button("Trailer 👉", new_page_url, use_container_width=True, help=new_page_url)

                    # if (i + 1) % num_columns == 0:
                    #     st.write('\n\n')
        except IndexError:
            st.error("An error occurred while processing the recommendation. Please try again.", icon="🚨")
