import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Title
st.title('My first app')

# Header
st.header('This is a header')

# Subheader
st.subheader('This is a subheader')

# Text
st.text('Hello Streamlit')

# Markdown
st.markdown('### This is a markdown')

# Error/Colorful Text
st.error('This is an error')
st.success('This is a success')
st.info('This is an info')
st.warning('This is a warning')

# Write
st.write('This is a write')

# Dataframe
df = pd.DataFrame({
    'Name': ['John', 'Jane', 'Doe'],
    'Age': [21, 22, 23]
})
st.dataframe(df)

# Table
st.table(df)

# Line Chart
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c']
)

st.line_chart(chart_data)

# Area Chart
st.area_chart(chart_data)

# Bar Chart
st.bar_chart(chart_data)

# Seaborn
st.write('Seaborn')
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 20, 30, 40, 50]
})
st.line_chart(df)

# Selectbox
option = st.selectbox('Which number do you like best?', df['x'])
'You selected: ', option

# Multiselect
options = st.multiselect('What are your favorite numbers?', df['x'])
'You selected: ', options

# Slider
age = st.slider('How old are you?', 0, 130, 25)
'You are: ', age

# Button
if st.button('Say hello'):
    st.write('Hello')

# Checkbox
if st.checkbox('Show/Hide'):
    st.write('Showing or hiding widget')

# Radio
genre = st.radio('What is your favorite genre?', ('Comedy', 'Drama', 'Documentary'))
'You selected: ', genre

# Text Input
title = st.text_input('Movie title', 'Life of Brian')
'Your movie title: ', title

# Number Input
number = st.number_input('Insert a number')