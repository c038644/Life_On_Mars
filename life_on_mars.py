import pandas as pd
import numpy as np
import streamlit as st

st.set_page_config(page_title='Life On Mars Dashboard',  layout='wide', page_icon=':Dashboard:')

#this is the header
 
#t1, t2 = st.columns((0.07,1)) 
t2 = st.columns((1))

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
