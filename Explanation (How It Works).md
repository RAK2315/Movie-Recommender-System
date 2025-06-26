## 🧠 Code Explanation (`Main.ipynb`)

The logic for generating movie recommendations is developed in the `Main.ipynb` notebook. Below is a breakdown of what your code does — based purely on your actual code without any modifications:

---

### 🔹 1. Import Required Libraries
```python
import pandas as pd
```
- Loads `pandas` for handling the CSV dataset and creating DataFrames.

---

### 🔹 2. Load the Dataset
```python
movies = pd.read_csv("dataset.csv")
```
- Loads the movie metadata into a DataFrame named `movies`.

---

### 🔹 3. Select Important Columns
```python
movies = movies[["id","title","overview","genre"]]
```
- Keeps only the columns needed for recommendations:
  - `id`: used for fetching posters later
  - `title`: displayed to the user
  - `overview` and `genre`: used for similarity

---

### 🔹 4. Create Combined Tags
```python
movies["tags"] = movies["overview"] + movies["genre"]
```
- Merges the overview and genre into a new column called `tags`.
- This combined text is used to compare movies.

---

### 🔹 5. Convert Text to Vectors
```python
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=10000,stop_words="english")
vectors = cv.fit_transform(movies["tags"]).toarray()
```
- Converts the `tags` column (combined genre + overview) into numeric feature vectors.
- `CountVectorizer` builds a vocabulary of the 5000 most frequent words.
- Each movie becomes a vector where each dimension counts the number of times a word appears.
- This step translates textual content into a **numerical form** that a machine can compare.

---

### 🔹 6. Calculate Cosine Similarity
```python
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
```
- Calculates **how similar each movie is to every other movie**.
- Cosine similarity measures the **angle between two movie vectors**.
- A value of **1 means perfect match**, 0 means no similarity.
- This results in a square matrix where `similarity[i][j]` represents how close movie i is to movie j.

---

### 🔹 7. Save Processed Files for Streamlit App
```python
import pickle
pickle.dump(movies, open("movies_list.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))
```
- Saves the final DataFrame and similarity matrix into `.pkl` (pickle) files.
- These files are loaded later in the `app.py` to serve recommendations.

---

> ⚠️ **Important Note:**  
> This GitHub repository does **not include** `movies_list.pkl` and `similarity.pkl`.  
> You must run the `Main.ipynb` notebook yourself to generate these files before using the app.



## 🌐 Code Explanation (`app.py`)

This is the **Streamlit frontend app** that loads preprocessed data and serves the movie recommendation system through a web UI. Here's a step-by-step breakdown:
Would be better if done in code editors like vs code

##
##
##



### 🔹 1. Import Required Libraries
```python
import streamlit as st
import pickle
import requests
```
- `streamlit`: used to build the interactive web interface.
- `pickle`: loads the saved movie data and similarity matrix.
- `requests`: fetches poster images from the TMDB API.

---

### 🔹 2. Load Preprocessed Files
```python
f1 = open("movies_list.pkl", "rb")
f2 = open("similarity.pkl", "rb")
movies = pickle.load(f1)
similarity = pickle.load(f2)
movies_list = movies["title"].values
```
- Loads the `.pkl` files created earlier.
- Extracts the list of all movie titles into `movies_list` for the dropdown menu.

---

### 🔹 3. Build Web UI
```python
st.header("Movie Recommendation System")
select_value = st.selectbox("Select Movie", movies_list)
```
- Adds a header and dropdown to let users pick a movie.

---

### 🔹 4. Fetch Poster Function
```python
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"
    except Exception as e:
        print(f"⚠️ Poster fetch failed for ID {movie_id} → {e}")
        return "https://via.placeholder.com/300x450?text=Error"
```
- Makes an API request to **TMDB** using the movie's `id`.
- If a valid `poster_path` is found, constructs a full poster URL.
- If not, returns a placeholder poster.
- This ensures the app doesn't break even if posters are missing or the API call fails.

> 🛠 Make sure to **generate your own TMDB API key** and paste it where indicated.

---

### 🔹 5. Recommend Function
```python
def recommend(movie1):
    index = movies[movies["title"] == movie1].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    
    rec_mov = []
    rec_poster = []

    for i in distance[1:11]:
        movies_id = movies.iloc[i[0]].id
        rec_mov.append(movies.iloc[i[0]].title)
        rec_poster.append(fetch_poster(movies_id))
    
    return rec_mov, rec_poster
```
- This function finds **10 most similar movies** to the selected one:
  - `similarity[index]` gives similarity scores of all movies with the selected movie.
  - `enumerate()` attaches indices to those scores.
  - `sorted(..., reverse=True)` ranks movies from most to least similar.
  - `distance[1:11]`: skips the first one (it's the same movie) and takes the next 10.
- It returns two lists:
  - `rec_mov`: Titles of recommended movies
  - `rec_poster`: Their poster image URLs

---

### 🔹 6. Display Recommendations
```python
if st.button("Recommend"):
    movie_name , movie_poster = recommend(select_value)
    
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
```
- When the "Recommend" button is clicked:
  - It runs the `recommend()` function.
  - Displays 10 recommendations with posters in **two rows of 5 columns each** using `st.columns`.

---

> ✅ This script must be run **after** generating the `.pkl` files using `Main.ipynb`.

> 🔴 **Note:** TMDB's API occasionally breaks or returns null posters. That’s not an error in your code — it's a server-side or data issue from TMDB.
