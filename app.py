import streamlit as st
import pickle
import numpy as np
import requests

movies = pickle.load(open('movies.pkl' , 'rb'))
movies_list = movies['title'].values

similarity = pickle.load(open('similarity.pkl' , 'rb'))

st.title('Movie Recommendation System')
selected_movie_name = st.selectbox(
     'Enter a name of the movie to get the suggestions',
     (movies_list))


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    similar_movies = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)[1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in similar_movies:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies , recommended_movies_poster


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=8392bef86d527087d70782c7b88b2bf9&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']


def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR60O2-muWvwgWvwmzklx-IydP5j0NZsLnHpg&usqp=CAU");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url()


if st.button('Recommend'):
    names , poster = recommend(selected_movie_name)

    col1 , col2 , col3 , col4 , col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(poster[0])

    with col2:
        st.text(names[1])
        st.image(poster[1])

    with col3:
        st.text(names[2])
        st.image(poster[2])

    with col4:
        st.text(names[3])
        st.image(poster[3])

    with col5:
        st.text(names[4])
        st.image(poster[4])