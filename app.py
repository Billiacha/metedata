import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
    df['year'] = df['publish_time'].dt.year
    return df

df = load_data()

# Title
st.title("CORD-19 Data Explorer")
st.write("Explore COVID-19 research papers from the CORD-19 dataset")

# Year filter
years = st.slider("Select year range:", 2015, 2023, (2019, 2021))
filtered = df[(df['year'] >= years[0]) & (df['year'] <= years[1])]

st.write(f"Showing {len(filtered)} papers between {years[0]} and {years[1]}")

# Publications over time
st.subheader("Publications by Year")
year_counts = filtered['year'].value_counts().sort_index()
fig, ax = plt.subplots()
ax.bar(year_counts.index, year_counts.values)
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = filtered['journal'].value_counts().head(10)
fig, ax = plt.subplots()
sns.barplot(y=top_journals.index, x=top_journals.values, ax=ax)
st.pyplot(fig)

# Word cloud
st.subheader("Word Cloud of Titles")
text = " ".join(filtered['title'].dropna())
wc = WordCloud(width=800, height=400, background_color="white").generate(text)
fig, ax = plt.subplots()
ax.imshow(wc, interpolation="bilinear")
ax.axis("off")
st.pyplot(fig)

# Show sample data
st.subheader("Sample Data")
st.dataframe(filtered.head(20))
