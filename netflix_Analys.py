import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from textblob import TextBlob
from IPython.display import display, HTML


# Set up Streamlit layout
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# Load data
dff = pd.read_csv('netflix_titles.csv')

# Prepare data for the first plot
z = dff.groupby(['rating']).size().reset_index(name='counts')
pieChart = px.pie(z, values='counts', names='rating',
                
                  color_discrete_sequence=px.colors.qualitative.Set3)

# Prepare data for the second plot
dff['director'] = dff['director'].fillna('No Director Specified')
filtered_directors = dff['director'].str.split(',', expand=True).stack()
filtered_directors = filtered_directors.to_frame()
filtered_directors.columns = ['Director']
directors = filtered_directors.groupby(['Director']).size().reset_index(name='Total Content')
directors = directors[directors.Director != 'No Director Specified']
directors = directors.sort_values(by=['Total Content'], ascending=False)
directorsTop5 = directors.head()
directorsTop5 = directorsTop5.sort_values(by=['Total Content'])
fig1 = px.bar(directorsTop5, x='Total Content', y='Director', width=500, height=500)


    



# Prepare data for the third plot
dff['cast'] = dff['cast'].fillna('No Cast Specified')
filtered_cast = dff['cast'].str.split(',', expand=True).stack()
filtered_cast = filtered_cast.to_frame()
filtered_cast.columns = ['Actor']
actors = filtered_cast.groupby(['Actor']).size().reset_index(name='Total Content')
actors = actors[actors.Actor != 'No Cast Specified']
actors = actors.sort_values(by=['Total Content'], ascending=False)
actorsTop5 = actors.head()
actorsTop5 = actorsTop5.sort_values(by=['Total Content'])
fig2 = px.bar(actorsTop5, x='Total Content', y='Actor', width=500, height=500)

# Prepare data for the fourth plot
df1 = dff[['type', 'release_year']]
df1 = df1.rename(columns={"release_year": "Release Year"})
df2 = df1.groupby(['Release Year', 'type']).size().reset_index(name='Total Content')
df2 = df2[df2['Release Year'] >= 2010]
fig3 = px.line(df2, x="Release Year", y="Total Content", color='type',
               title='', width=500, height=500)

# Prepare data for the fifth plot
dfx = dff[['release_year', 'description']]
dfx = dfx.rename(columns={'release_year': 'Release Year'})
for index, row in dfx.iterrows():
    z = row['description']
    testimonial = TextBlob(z)
    p = testimonial.sentiment.polarity
    if p == 0:
        sent = 'Neutral'
    elif p > 0:
        sent = 'Positive'
    else:
        sent = 'Negative'
    dfx.loc[[index, 2], 'Sentiment'] = sent

dfx = dfx.groupby(['Release Year', 'Sentiment']).size().reset_index(name='Total Content')
dfx = dfx[dfx['Release Year'] >= 2010]
fig4 = px.bar(dfx, x="Release Year", y="Total Content", color="Sentiment",
              width=500, height=500)

# Create Streamlit app

st.title('**:violet[Netflix Dashboard]**' ":100:")


st.write("I’ll take a look at some very important models of Netflix data to understand what’s best for their business. Some of the most important tasks that we can analyze from Netflix data are: understand what content is available understand the similarities between the content understand the network between actors and directors what exactly Netflix is focusing on and sentiment analysis of content available on Netflix.")


# Display the first plot
st.subheader("Distribution of Content Ratings on Netflix")
st.plotly_chart(pieChart)

# Display the second and third plots in two columns with spacing
col1, col2 = st.columns(2)


with col1:
    st.subheader("Top 5 Directors on Netflix")
    st.plotly_chart(fig1)
    
    st.subheader("Trend of content produced over the years on Netflix")
    st.plotly_chart(fig3)

  
with col2:
    st.subheader("Top 5 Actors on Netflix")
    st.plotly_chart(fig2)
    
    
    st.subheader("Sentiment of content on Netflix")
    st.plotly_chart(fig4)