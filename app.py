import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for j in distance[1:6]:
        recommended_movie_names.append(movies.iloc[j[0]].title)
        recommended_movie_posters.append(fetch_poster(movies.iloc[j[0]].movie_id))
    return recommended_movie_names, recommended_movie_posters


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8'
                            f'&language=en-US')
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


st.title("Movies Recommender System")

option = st.selectbox('Search your Taste', sorted(movies['title'].values))


if st.button('Recommend'):
    names, posters = recommend(option)

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
