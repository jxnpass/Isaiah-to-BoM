# %%
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

url = 'https://github.com/esnt/Data/raw/main/Names/popular_names.csv'
df = pd.read_csv(url)




# %%
# DASHBOARD 1
st.title('Popular Names')

select_name = st.text_input("Enter a name", "John") # default is John
name_df = df[df['name'] == select_name]
if name_df.empty:
    st.write('No data for this name')
else: 
    fig = px.line(name_df, x = 'year', y = 'n', color = 'sex',
                  color_discrete_sequence = px.colors.qualitative.Set3)
    st.plotly_chart(fig)



# %%
# DASHBOARD 2

select_year = st.selectbox('Select a year', df['year'].unique())

year_df = df[df['year'] == select_year]
girl_names = (year_df[year_df['sex'] == 'F'].sort_values(by = 'n', ascending = False).head(5)['name']).reset_index(drop = True)
boy_names = (year_df[year_df['sex'] == "M"].sort_values(by = 'n', ascending = False).head(5)['name']).reset_index(drop = True)
top_names = pd.concat([girl_names, boy_names], axis=1)
top_names.columns = ['girl','boy']

st.write(f"Top names in {select_year}")
st.dataframe(top_names)


