import streamlit as st
import pickle
import requests

# Streamlit setup
st.set_page_config(
    page_title="Cine Magic - Genre Wise Movie",
    page_icon="🤔",
    layout="wide",
)

# Load movies data from pickle file
with open('movie-files/genres_movie_list.pkl', 'rb') as f:
    Movies = pickle.load(f)

Movies = Movies.sort_values('rating', ascending=False)


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
            st.warning("Error: 'poster_path' not found in API response.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred in fetch_Poster: {str(e)}")
        print(f"An error occurred in fetch_Poster: {str(e)}")
        return None

# Function to fetch movie and video links
def fetch_links(id):
    try:
        url = 'https://api.themoviedb.org/3/movie/{}/videos?api_key=c7ec19ffdd3279641fb606d19ceb9bb1'.format(id)
        response = requests.get(url)
        response.raise_for_status()
        link_data = response.json()

        if 'results' in link_data and link_data['results']:
            link = link_data['results'][0].get('key', '')
            return link
        else:
            st.warning("Error: No video link found in API response.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred in fetch_links: {str(e)}")
        print(f"An error occurred in fetch_links: {str(e)}")
        return None

# Function to get Genre Wise movies
def getGenreWise_movies(genres, limit):
    movie_list = Movies.to_dict(orient='records')

    popular_movies = []
    recommended_movies_poster = []
    links = []
    movie_id = []
    genre_set = set(genres)  # Convert genres to a set for faster membership tests

    for i in movie_list:
        # Check if any selected genre is in the movie's genres
        if any(selected_genre in i['genres'] for selected_genre in genre_set):
            id = i['id']
            popular_movies.append(i['title'])
            recommended_movies_poster.append(fetch_Poster(id))
            links.append(fetch_links(id))
            movie_id.append(id)

        if len(popular_movies) == limit:
                break

    return popular_movies, recommended_movies_poster, links, movie_id


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit layout
with st.container(border=True):
    st.title("Genre Wise Movies")
options = st.multiselect(
    'Select Your Genre',
    ['Action', 'Adventure', 'Science Fiction', 'Crime', 'Drama', 'Romance', 'Fantasy', 'Horror', 'Family', 'Thriller'])


limit = st.slider("Set limit", 1, 25, 5)

with st.container():

    titles, posters, links, id = getGenreWise_movies(options, limit)
    num_columns = 5
    columns = st.columns(num_columns)
    
    for i in range(len(titles)):
        with columns[i % num_columns]:
            st.image(posters[i], use_column_width=True)
            link = titles[i]

            if links[i]:
                titles[i] = titles[i].replace(" ", "-").replace(".", "-").replace(":", "").lower()
                home = "https://www.themoviedb.org/movie/{}-{}".format(id[i], titles[i])
                st.write(f"[{link}]({home})")

                new_page_url = 'https://www.youtube.com/watch?v={}'.format(links[i])
                st.link_button("Trailer 👉", new_page_url, use_container_width=True, help=new_page_url)

            # If you want to add some space between columns on mobile, you can uncomment the next line
            # st.write('\n\n')
