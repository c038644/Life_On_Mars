import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title='Life On Mars Dashboard',  layout='wide', page_icon=':Dashboard:')

#this is the header
 
t1, t2 = st.columns((0.07,1)) 

t2.title("Life On Mars Dashboard")

with st.spinner('Updating Report...'):
    
    Planet_Selection = pd.read_csv("./Planet_Names.csv")
    Planet_Selection = Planet_Selection.drop(columns=['0'])
    
    Exoplanet_df = pd.read_csv("./Exoplanet_with_Continent.csv")
    #Exoplanet_df = Exoplanet_df.drop(columns=['Unnamed: 0'])

    Planet = st.selectbox('Select Planet', Planet_Selection, help = 'Filter report to show only one exoplanet')


    if Planet:
        Selected_Planet = Exoplanet_df.loc[Exoplanet_df['Planet Name'] == Planet]
        st.write(Selected_Planet)

g1, g2 = st.columns((1,2))    

fig1 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = Planet_Selection.iat[0,4],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Life Ranking", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 0.33], 'color': 'red'},
                {'range': [0.34, 0.66], 'color': 'orange'},
                {'range': [0.67, 1], 'color': 'green'}]}))

g1.plotly_chart(fig1, use_container_width=True)
