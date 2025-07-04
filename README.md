# 🎬 Movie Recommender System

A content-based movie recommendation system built using Python, Streamlit, and the TMDB API.  
The app recommends 10 movies similar to the one selected by the user, and fetches their posters dynamically.

---

## 🚀 Features

- Select a movie and get 10 recommendations
- Posters are fetched in real-time using the TMDB API
- Fully interactive web UI using Streamlit
- Uses NLP techniques to analyze movie similarity

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** (for frontend UI)
- **pandas** (for data manipulation)
- **scikit-learn** (`CountVectorizer`, `cosine_similarity`)
- **pickle** (to store and load processed data)
- **TMDB API** (to fetch movie posters dynamically)

---

## 📂 Dataset Used

- Source: `dataset.csv`
- Contains information like:
  - `title`, `genres`, `cast`, `crew`, `overview`, `keywords`, and `id` (TMDB ID)
- Preprocessed and stored in `movies_list.pkl`
- Similarity matrix stored in `similarity.pkl`

---

## 🧠 Recommendation Logic

1. All relevant movie fields (`genres`, `cast`, `overview`, etc.) are combined into a single `tags` column.
2. `CountVectorizer` is used to convert tags into a vector representation.
3. `cosine_similarity` compares movies by their tag vectors.
4. The most similar 10 movies are selected for any given input.

---

### Read Documentation file to understand the code

