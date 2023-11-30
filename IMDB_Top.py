import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page title and icon
st.set_page_config(page_title="IMDb Top Movies Analysis", page_icon="🎬")

# Load the dataset from the CSV file
df = pd.read_csv("IMDB Top.csv")

# Remove commas and quotes from the 'year' column
df['year'] = df['year'].astype(str).str.replace(',', '').str.replace('"', '')

# Convert the 'year' column to numeric
df['year'] = pd.to_numeric(df['year'], errors='coerce')

# Replace empty strings with 0 in the 'budget' column
df['budget'] = df['budget'].replace('', '0')

# Remove non-numeric characters from the 'budget' column
df['budget'] = df['budget'].replace('[^\d.]', '0', regex=True)

# Convert the 'budget' column to float
df['budget'] = df['budget'].astype(float)

# Sidebar for user input
st.sidebar.title("IMDb Top Movies Analysis")

# Dropdown for selecting a genre
selected_genre = st.sidebar.selectbox("Select Genre", df['genre'].unique())

# Slider for filtering movies based on minimum rating
min_rating = st.sidebar.slider("Minimum Rating", 1.0, 10.0, 5.0, 0.1)

# Filter data based on user input
filtered_df = df[(df['genre'] == selected_genre) & (df['rating'] >= min_rating)]

# Display filtered data
st.write(f"### Filtered Data for {selected_genre} Genre and Minimum Rating {min_rating}")
st.dataframe(filtered_df)

# Bar chart for average ratings and box office by selected movies
st.write(f"### Ratings and Box Office for Selected Movies")
bar_fig = px.bar(
    filtered_df, x='name', y=['rating', 'box_office'],
    labels={'rating': 'Rating', 'box_office': 'Box Office'},
    title=f'Ratings and Box Office for Selected Movies',
    hover_data={'name': True, 'rating': ':.2f', 'box_office': ':,.2f'},
)
st.plotly_chart(bar_fig)

# Scatter plot for the relationship between budget and box office
st.write(f"### Relationship between Budget and Box Office")
scatter_fig = px.scatter(
    filtered_df, x='budget', y='box_office',
    labels={'budget': 'Budget', 'box_office': 'Box Office'},
    title=f'Relationship between Budget and Box Office',
    hover_data={'name': True},
)
st.plotly_chart(scatter_fig)

# Histogram for the distribution of ratings
st.write(f"### Distribution of Ratings")
histogram_fig = px.histogram(
    filtered_df, x='rating',
    labels={'rating': 'Rating'},
    title=f'Distribution of Ratings',
    nbins=20,
)
st.plotly_chart(histogram_fig)

# Treemap for Budget and Box Office by Genre
treemap_fig = px.treemap(
    filtered_df, path=['genre'], values='budget',
    labels={'budget': 'Budget', 'genre': 'Genre'},
    title='Treemap: Budget Distribution by Genre',
)
st.plotly_chart(treemap_fig)
