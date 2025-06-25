# To make web application in python we import streamlit library
import streamlit as st
import pickle
import requests

f1=open("movies_list.pkl","rb")
f2=open("similarity.pkl","rb")
movies = pickle.load(f1)
similarity = pickle.load(f2) 
movies_list=movies["title"].values

st.header("Movie Recommendation System")
select_value=st.selectbox("Select Movie",movies_list)

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=60acbbd80f6bfc395f37ff2d2e971218&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            full_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_url
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except Exception as e:
        print(f"⚠️ Poster fetch failed for ID {movie_id} → {e}")
        return "https://via.placeholder.com/300x450?text=Error"




def recommend(movie1):
    index = movies[movies["title"]==movie1].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True,key =lambda vector: vector[1])
    rec_mov=[]   
    rec_poster=[]
    for i in distance[1:11]:
        movies_id= movies.iloc[i[0]].id
        rec_mov.append(movies.iloc[i[0]].title)
        rec_poster.append(fetch_poster(movies_id))
    return rec_mov, rec_poster
 
if st.button("Recommend"):
    movie_name , movie_poster= recommend(select_value)
    cols = st.columns(5)
for i in range(5):
    with cols[i]:
        st.text(movie_name[i])
        st.image(movie_poster[i])

cols2 = st.columns(5)
for i in range(5, 10):
    with cols2[i - 5]:
        st.text(movie_name[i])
        st.image(movie_poster[i])
