import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Life On Mars Dashboard',  layout='wide', page_icon=':Dashboard:')

#this is the header
 
t1, t2 = st.columns((1,1)) 

t1.title("Life On Mars Dashboard")
  
Exoplanet_df = pd.read_csv("./Exoplanet_with_Continent.csv")

# Display the slider in the sidebar for the user to choose the minimum planet radius

Input = pd.read_csv("./Input.csv")
Input_Selector = st.sidebar.selectbox('Select Input Option', Input, help = 'Filter report to show only one feature')

min_radius = Exoplanet_df['Planet Radius [Earth Radius]'].min()
max_radius = Exoplanet_df['Planet Radius [Earth Radius]'].max()
min_mass = Exoplanet_df['Planet Mass [Earth Mass]'].min()
max_mass = Exoplanet_df['Planet Mass [Earth Mass]'].max()
min_temp = Exoplanet_df['Planet Temperature'].min()
max_temp = Exoplanet_df['Planet Temperature'].max()

if Input_Selector == 'Slider':
 
 planet_radius_options = st.sidebar.slider('Select Required Planet Radii:', value = (min_radius, max_radius))

 planet_mass_options = st.sidebar.slider('Select Required Planet Masses:', value = (min_mass, max_mass))

 planet_temp_options = st.sidebar.slider('Select Required Temperature Range:', value = (min_temp, max_temp))

 Min_flitered_df = Exoplanet_df.loc[Exoplanet_df['Planet Radius [Earth Radius]'] > planet_radius_options[0]]
 flitered_df = Min_flitered_df.loc[Min_flitered_df['Planet Radius [Earth Radius]'] < planet_radius_options[1]]

 Min_flitered_df = flitered_df.loc[flitered_df['Planet Mass [Earth Mass]'] > planet_mass_options[0]]
 flitered_df = Min_flitered_df.loc[Min_flitered_df['Planet Mass [Earth Mass]'] < planet_mass_options[1]]

 Min_flitered_df = flitered_df.loc[flitered_df['Planet Temperature'] > planet_temp_options[0]]
 flitered_df = Min_flitered_df.loc[Min_flitered_df['Planet Temperature'] < planet_temp_options[1]]
 
elif Input_Selector == 'Number Input':
  min_radius = st.sidebar.number_input('Minimum Planet Radius:', Input_min_radius)
  max_radius = st.sidebar.number_input('Maximum Planet Radius:', Input_max_radius)
  min_mass = st.sidebar.number_input('Minimum Planet Mass:', Input_min_mass)
  max_mass = st.sidebar.number_input('Maximum Planet Mass:', Input_max_mass)
  min_temp = st.sidebar.number_input('Minimum Planet Temperature:', Input_min_temp)
  max_temp = st.sidebar.number_input('Maximum Planet Temperature:', Input_max_temp)

  Min_flitered_df = Exoplanet_df.loc[Exoplanet_df['Planet Radius [Earth Radius]'] > min_radius]
  flitered_df = Min_flitered_df.loc[Min_flitered_df['Planet Radius [Earth Radius]'] < max_radius]

  Min_flitered_df = flitered_df.loc[flitered_df['Planet Mass [Earth Mass]'] > min_mass]
  flitered_df = Min_flitered_df.loc[Min_flitered_df['Planet Mass [Earth Mass]'] < max_mass]

  Min_flitered_df = flitered_df.loc[flitered_df['Planet Mass [Earth Mass]'] > min_temp]
  flitered_df = Min_flitered_df.loc[Min_flitered_df['Planet Mass [Earth Mass]'] < max_temp]
 
st.sidebar.write('You have selected', flitered_df.shape[0], 'planets')

#Planet = st.selectbox('Select Planet', flitered_df['Planet Name'], help = 'Filter report to show only one exoplanet')
#Selected_Planet = Exoplanet_df.loc[Exoplanet_df['Planet Name'] == Planet]

#if Selected_Planet.empty:
# st.write('No matching planet found.')
 #st.experimental_rerun()
#else:
# g1, g2 = st.columns((1,3))    

# fig1 = go.Figure(go.Indicator(
#        mode = "gauge+number+delta",
#        value = Selected_Planet.iat[0,3],
#        domain = {'x': [0, 1], 'y': [0, 1]},
#        title = {'text': "Life Ranking", 'font': {'size': 24}},
#        gauge = {
#            'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "darkblue"},
#            'bar': {'color': "black"},
#            'bgcolor': "white",
#            'borderwidth': 2,
#            'bordercolor': "gray",
#            'steps': [
#                {'range': [0, 0.33], 'color': 'red'},
#                {'range': [0.34, 0.66], 'color': 'orange'},
#                {'range': [0.67, 1], 'color': 'green'}]}))

#g1.plotly_chart(fig1, use_container_width=True)

g1 = st.columns((1,))

Feature_List = pd.read_csv("./Feature_List.csv")

Feature = st.sidebar.selectbox('Select Feature', Feature_List, help = 'Filter report to show only one feature')

fig1 = px.scatter(flitered_df, x = 'Planet Name', y = Feature)

g1[0].plotly_chart(fig1, use_container_width=True)
