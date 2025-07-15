import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Configuration
# -----------------------------
API_KEY = 'YOUR_API_KEY'  # Replace with your TMDb API key
BASE_URL = 'https://api.themoviedb.org/3'

# -----------------------------
# Fetch Trending Movies
# -----------------------------
def fetch_trending_movies():
    url = f'{BASE_URL}/trending/movie/week?api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['results']

# -----------------------------
# Process Movie Data
# -----------------------------
def process_data(movies):
    movie_titles = []
    popularity_scores = []
    genres = []
    genre_map = fetch_genre_mapping()

    for movie in movies:
        movie_titles.append(movie['title'])
        popularity_scores.append(movie['popularity'])
        genre_ids = movie['genre_ids']
        if genre_ids:
            genres.append(genre_map.get(genre_ids[0], 'Unknown'))
        else:
            genres.append('Unknown')

    df = pd.DataFrame({
        'Title': movie_titles,
        'Popularity': popularity_scores,
        'Genre': genres
    })
    return df

# -----------------------------
# Fetch Genre Mapping
# -----------------------------
def fetch_genre_mapping():
    url = f'{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US'
    response = requests.get(url)
    genres = response.json()['genres']
    genre_map = {genre['id']: genre['name'] for genre in genres}
    return genre_map

# -----------------------------
# Visualization Functions
# -----------------------------
def plot_top_movies(df):
    top_movies = df.sort_values(by='Popularity', ascending=False).head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Popularity', y='Title', data=top_movies, palette='viridis')
    plt.title('Top 10 Trending Movies')
    plt.xlabel('Popularity')
    plt.ylabel('Movie Title')
    plt.show()

def plot_genre_distribution(df):
    plt.figure(figsize=(8, 8))
    genre_counts = df['Genre'].value_counts()
    plt.pie(genre_counts, labels=genre_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set2'))
    plt.title('Genre Distribution of Trending Movies')
    plt.show()

# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    movies = fetch_trending_movies()
    df = process_data(movies)
    print(df.head())  # Preview the data

    # Visualizations
    plot_top_movies(df)
    plot_genre_distribution(df)
