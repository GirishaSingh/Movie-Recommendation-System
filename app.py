import streamlit as st
import pickle
import requests
from io import BytesIO
import gdown


# Function to fetch the similarity matrix from Google Drive
@st.cache_resource
def fetch_similarity_from_google_drive():
    url = 'https://drive.google.com/uc?export=download&id=1Bs0b2ACEfhksHyhw_zBIVnl6P3AlBHv1'
    response = gdown.download(url, output=None, quiet=False)
    similar = pickle.load(open(response, 'rb'))
    return similar


def recommend(movie):
    movie_index = movies_[movies_['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movie_list:
        movie_title = movies_.iloc[i[0]].title
        recommended_movies.append(movie_title)
        recommended_movies_poster.append(fetch_poster(movie_title))
    return recommended_movies, recommended_movies_poster


# Function to fetch movie poster from OMDb API
def fetch_poster(movie_title):
    api_key = 'f7f7a8c8'
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    if 'Poster' in data and data['Poster'] != 'N/A':
        return data['Poster']
    else:
        return None


# Load data
movies_ = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_['title'].values

# Fetch similarity matrix from Google Drive
similarity = fetch_similarity_from_google_drive()

if similarity is not None:
    st.title('Movie Recommendation System')

    movie_name = st.selectbox('Select a movie:', movies_list)

    if st.button('Recommend'):
        names, posters = recommend(movie_name)

        col1, col2, col3, col4, col5 = st.columns(5)

        for col, name, poster in zip([col1, col2, col3, col4, col5], names, posters):
            with col:
                st.markdown(f"""
                    <div style="text-align: center;">
                        <img src="{poster}" style="width: 100%; height: auto; border-radius: 10px;">
                        <p style="font-size: 14px; color: black; word-wrap: break-word;">{name}</p>
                    </div>
                """, unsafe_allow_html=True)

    # CSS to ensure alignment and theming
    st.markdown(
        """
        <style>
        /* General background and text styling */

        /* Selectbox styling */
        .css-2b097c-container {
            color: black !important;
        }
        /* Button styling */
        .stButton button {
            background-color: #e50914;
            color: white;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #f40612;
            color: white;
        }
        /* Center alignment for markdown containers */
        [data-testid="stMarkdownContainer"] {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        /* Element container styling for better alignment */
        .element-container {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.error("Could not load the similarity matrix. Please check the file and try again.")
