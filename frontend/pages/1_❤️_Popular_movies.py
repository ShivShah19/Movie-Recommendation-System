import streamlit as st
import pickle
import requests


# # Streamlit setup
st.set_page_config(
    page_title="Cine Magic - Popular Movies",
    page_icon="❤️",
    layout="wide",
)

# Load movies data from pickle file
with open('movie-files/Best_movies.pkl', 'rb') as f:
    Movies = pickle.load(f)

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
        print(f"An error occurred in fetch_movies: {str(e)}")
        st.error(f"An error occurred in fetch_movies: {str(e)}")
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
        print(f"An error occurred in fetch_links: {str(e)}")
        st.error(f"An error occurred in fetch_links: {str(e)}")
        return None


# Function to get Popular Movies
def getPopular_movies(range):
    movie_list = Movies.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries

    polular_movies = []
    popular_movies_poster = []
    links = []
    id = []

    for i in movie_list[0:range]:
        movie_id = i['id']
        polular_movies.append(i['title'])
        popular_movies_poster.append(fetch_Poster(movie_id))
        links.append(fetch_links(movie_id))
        id.append(movie_id)

    return polular_movies, popular_movies_poster, links, id
    


with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Streamlit layout
st.title("Popular Movies")
limit = st.slider("Set limit", 1,100,10)

with st.container():
        titles, posters, links, id = getPopular_movies(limit)
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
                    # st.write(f"[Trailer]({new_page_url})")
                    st.link_button("Trailer 👉", new_page_url, use_container_width = True, help=new_page_url)


                # if (i + 1) % num_columns == 0:
                #     st.write('\n\n')
