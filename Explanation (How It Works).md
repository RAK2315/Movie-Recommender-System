
# Explanation (How It Works)


---
## 🧠 Code Explanation (Jupyter Notebook)

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
cv = CountVectorizer(max_features=5000)
vectors = cv.fit_transform(movies["tags"]).toarray()
```
- Converts the `tags` into numeric vectors using `CountVectorizer`.
- Each movie becomes a 5000-dimensional vector based on its word counts.

---

### 🔹 6. Calculate Cosine Similarity
```python
from sklearn.metrics.pairwise import cosine_similarity
similarity = cosine_similarity(vectors)
```
- Computes pairwise cosine similarity between movie vectors.
- A higher value means more similar content.

---

### 🔹 7. Save Processed Files for Streamlit App
```python
import pickle
pickle.dump(movies, open("movies_list.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))
```
- Saves the final DataFrame and similarity matrix into `.pkl` files.
- These files are used by the `app.py` Streamlit frontend.

---

> ⚠️ **Important Note:**  
> This GitHub repository does **not include** `movies_list.pkl` and `similarity.pkl`.  
> You must run the `Main.ipynb` notebook yourself to generate these files before using the app.



---

## 🌐 Code Explanation (`app.py`)

This is the **Streamlit frontend app** that loads preprocessed data and serves the movie recommendation system through a web UI. Here's a step-by-step breakdown:

---

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
- Loads the movie metadata and cosine similarity matrix.
- Extracts all movie titles into a list for the dropdown.

---

### 🔹 3. Build Web UI
```python
st.header("Movie Recommendation System")
select_value = st.selectbox("Select Movie", movies_list)
```
- Displays a main heading and dropdown menu with movie titles.

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
- Uses TMDB API to fetch poster image for a given movie ID.
- Returns a placeholder if poster is missing or the request fails.
- NOTE: Generate your own api key from tmdb api and enter it in the code above

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
- Finds the index of the selected movie.
- Gets the 10 most similar movies from the similarity matrix.
- Collects their titles and poster URLs.

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
- On clicking the **Recommend** button:
  - Calls the `recommend()` function.
  - Displays the 10 recommended movies and their posters in two rows (5 per row).

---

> ✅ This script must be run **after** generating the `.pkl` files using `Main.ipynb`.

> NOTE: TMDB poster links have been broken for a while now so there is a good chance alot of the posters won't loan their poster images, this is a problem on thier hand not in the code.


