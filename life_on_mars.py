import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Life On Mars Dashboard',  layout='wide', page_icon=':Dashboard:')

#this is the header
 
t1, t2 = st.columns((1,1)) 

t1.title("Life On Mars Dashboard")

with st.spinner('Updating Report...'):
    
    Planet_Selection = pd.read_csv("./Planet_Names.csv")
    Planet_Selection = Planet_Selection.drop(columns=['0'])
    
    Exoplanet_df = pd.read_csv("./Exoplanet_with_Continent.csv")
    #Exoplanet_df = Exoplanet_df.drop(columns=['Unnamed: 0'])

    Planet = st.selectbox('Select Planet', Planet_Selection, help = 'Filter report to show only one exoplanet')
 
    if Planet:
        Selected_Planet = Exoplanet_df.loc[Exoplanet_df['Planet Name'] == Planet]
        st.write(Selected_Planet)

planet_radius_min_options = st.sidebar.slider('Select Minimum Planet Radius:', 
                                              min_value=[Exoplanet_df['Planet Radius [Earth Radius]'].min(), 
                                              max_value=[Exoplanet_df['Planet Radius [Earth Radius]'].max(), 
                                              value=0, 
                                              step=100)

#Planet_Radius_Min_options = st.sidebar.number_input('Planet_Radius_Min =')   

#flitered_df = st.sidebar.multiselect('Minimum Planet Radius', Exoplanet_df.loc[Exoplanet_df['Planet Radius [Earth Radius]'] > Planet_Radius_Min_options])
flitered_df = Exoplanet_df.loc[Exoplanet_df['Planet Radius [Earth Radius]'] > Planet_Radius_Min_options]
flitered_df.shape
#Feature = st.selectbox('Select Feature', Feature_List, help = 'Filter report to show only one feature')

g1, g2 = st.columns((1,3))    

fig1 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = Selected_Planet.iat[0,3],
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

#fig2 = px.scatter(Exoplanet_df, x = 'Planet Name', y = Feature)

#g2.plotly_chart(fig2, use_container_width=True)
