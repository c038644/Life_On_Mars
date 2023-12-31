import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='Life On Mars Dashboard',  layout='wide', page_icon=':Dashboard:')

t1, t2 = st.columns((1,1)) 

t1.title("Life On Mars Dashboard")

#Read Input File
Exoplanet_df = pd.read_csv("./exoplanets_cleaned.csv")
Exoplanet_df = Exoplanet_df.drop(columns=['Unnamed: 0'])

#Generate New Features
Exoplanet_df['Lum_Max'] = np.sqrt(10**(Exoplanet_df['Star luminosity'])/0.53)
Exoplanet_df['Lum_Min'] = np.sqrt(10**(Exoplanet_df['Star luminosity'])/1.1)
Exoplanet_df['gravitational_pressure'] = Exoplanet_df["Planet Mass [Earth Mass]"] / (Exoplanet_df['Planet Radius [Earth Radius]'] * Exoplanet_df['Planet Radius [Earth Radius]']) 
Exoplanet_df['atmospheric_pressure'] = Exoplanet_df['gravitational_pressure'] * Exoplanet_df['gravitational_pressure']
Exoplanet_df['Score'] = 0

#Calculate Goldilocks Score for each Planet
Exoplanet_df.loc[(Exoplanet_df["Equilibrium Temperature [K]"] > 258) & (Exoplanet_df["Equilibrium Temperature [K]"] < 395), "Score"] += 20
Exoplanet_df.loc[(Exoplanet_df["Planet Mass [Earth Mass]"] > 0.5) & (Exoplanet_df["Planet Mass [Earth Mass]"] < 7), "Score"] += 20
Exoplanet_df.loc[(Exoplanet_df['Orbital Radius'] > Exoplanet_df['Lum_Min']) & (Exoplanet_df['Orbital Radius'] < Exoplanet_df['Lum_Max']), "Score"] += 20
Exoplanet_df.loc[(Exoplanet_df['atmospheric_pressure'] > 0.5) & (Exoplanet_df['atmospheric_pressure'] < 2), "Score"] += 20

#Drop NaN's and create a copy
Exoplanet_df.dropna()
filtered_df = Exoplanet_df.copy()

Input_Selector = st.sidebar.selectbox('Select Input Option', ("Choose an option:", 'Slider Search', 'Number Input Search', 'Goldilocks Calculator'), placeholder = "Choose an option")

if Input_Selector == 'Slider Search':

    #Set Min and Max for the sliders
    min_radius = Exoplanet_df['Planet Radius [Earth Radius]'].min()
    max_radius = Exoplanet_df['Planet Radius [Earth Radius]'].max()
    min_mass = Exoplanet_df['Planet Mass [Earth Mass]'].min()
    max_mass = Exoplanet_df['Planet Mass [Earth Mass]'].max()
    min_temp = Exoplanet_df['Equilibrium Temperature [K]'].min()
    max_temp = Exoplanet_df['Equilibrium Temperature [K]'].max()

    #Create sliders
    planet_radius_options = st.sidebar.slider('Select Required Planet Radii:', value = (min_radius, max_radius))
    planet_mass_options = st.sidebar.slider('Select Required Planet Masses:', value = (min_mass, max_mass))
    planet_temp_options = st.sidebar.slider('Select Required Temperature Range:', value = (min_temp, max_temp))

    #Create dataframe with slider selections
    Min_radius_flitered_df = Exoplanet_df.loc[Exoplanet_df['Planet Radius [Earth Radius]'] > planet_radius_options[0]]
    flitered_radius_df = Min_radius_flitered_df.loc[Min_radius_flitered_df['Planet Radius [Earth Radius]'] < planet_radius_options[1]]

    Min_mass_flitered_df = flitered_radius_df.loc[flitered_radius_df['Planet Mass [Earth Mass]'] > planet_mass_options[0]]
    flitered_mass_df = Min_mass_flitered_df.loc[Min_mass_flitered_df['Planet Mass [Earth Mass]'] < planet_mass_options[1]]

    Min_temp_flitered_df = flitered_mass_df.loc[flitered_mass_df['Equilibrium Temperature [K]'] > planet_temp_options[0]]
    flitered_df = Min_temp_flitered_df.loc[Min_temp_flitered_df['Equilibrium Temperature [K]'] < planet_temp_options[1]]

    #Number of planets selected
    st.sidebar.write('You have selected', flitered_df.shape[0], 'planets')

    #Set one column
    g1 = st.columns((1,))

    #Create List of features from dataframe
    Feature_List = flitered_df.columns

    Feature = st.sidebar.selectbox('Select Feature', Feature_List, help = 'Filter report to show only one feature')

    fig1 = px.scatter(flitered_df, x = 'Planet Name', y = Feature)

    g1[0].plotly_chart(fig1, use_container_width=True)

elif Input_Selector == 'Number Input Search':

    #Set Min and Max for the number input search
    min_radius = Exoplanet_df['Planet Radius [Earth Radius]'].min()
    max_radius = Exoplanet_df['Planet Radius [Earth Radius]'].max()
    min_mass = Exoplanet_df['Planet Mass [Earth Mass]'].min()
    max_mass = Exoplanet_df['Planet Mass [Earth Mass]'].max()
    min_temp = Exoplanet_df['Equilibrium Temperature [K]'].min()
    max_temp = Exoplanet_df['Equilibrium Temperature [K]'].max()

    #Create number input boxes
    Input_min_radius = st.sidebar.number_input('Minimum Planet Radius:', min_radius)
    Input_max_radius = st.sidebar.number_input('Maximum Planet Radius:', min_radius)
    Input_min_mass = st.sidebar.number_input('Minimum Planet Mass:', min_mass)
    Input_max_mass = st.sidebar.number_input('Maximum Planet Mass:', min_mass)
    Input_min_temp = st.sidebar.number_input('Minimum Planet Temperature:', min_temp)
    Input_max_temp = st.sidebar.number_input('Maximum Planet Temperature:', min_temp)

    #Create dataframe with input box selections
    Min_flitered_df = Exoplanet_df.loc[Exoplanet_df['Planet Radius [Earth Radius]'] > Input_min_radius]
    flitered_df = Min_flitered_df.loc[Min_flitered_df['Planet Radius [Earth Radius]'] < Input_max_radius]

    Min_flitered_df = flitered_df.loc[flitered_df['Planet Mass [Earth Mass]'] > Input_min_mass]
    flitered_df = Min_flitered_df.loc[Min_flitered_df['Planet Mass [Earth Mass]'] < Input_max_mass]

    Min_flitered_df = flitered_df.loc[flitered_df['Equilibrium Temperature [K]'] > Input_min_temp]
    flitered_df = Min_flitered_df.loc[Min_flitered_df['Equilibrium Temperature [K]'] < Input_max_temp]

    #Number of planets selected
    st.sidebar.write('You have selected', flitered_df.shape[0], 'planets')

    g1 = st.columns((1,))

    Feature_List = flitered_df.columns

    Feature = st.sidebar.selectbox('Select Feature', Feature_List, help = 'Filter report to show only one feature')

    fig1 = px.scatter(flitered_df, x = 'Planet Name', y = Feature)

    g1[0].plotly_chart(fig1, use_container_width=True)

elif Input_Selector == 'Goldilocks Calculator':

    #List of planets sorted by decending Goldlocks score 
    Planet_Selection = filtered_df.sort_values(by='Score', ascending=False)['Planet Name']

    Planet = st.selectbox('Select Planet', Planet_Selection, help = 'Filter report to show only one feature')
    Selected_Planet = Exoplanet_df.loc[Exoplanet_df['Planet Name'] == Planet]

    #Print line of selected dataframe
    st.write(Selected_Planet)

    #Column setup
    g1, g2 = st.columns((1, 1))

    #Speedometer
    fig1 = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = Selected_Planet.iat[0,14],
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Life Ranking", 'font': {'size': 24}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 33], 'color': 'red'},
                {'range': [34, 66], 'color': 'orange'},
                {'range': [67, 100], 'color': 'green'}]}))

    g1.plotly_chart(fig1, use_container_width=True)

    with g2:
        st.write('Does the planet have a solid surface?')
        if ((Selected_Planet['Planet Mass [Earth Mass]'] > 0.5) & (Selected_Planet['Planet Mass [Earth Mass]'] < 7)).all():
            st.write('Yes !')
        else:
            st.write('No')
        
        st.write('Does the planet have a pressure between 0.5 and 2 atmospheres?')
        if ((Selected_Planet['atmospheric_pressure'] > 0.5) & (Selected_Planet['atmospheric_pressure'] < 2)).all():
            st.write('Yes !')
            st.write('Is it possible the planet has carbon, oxygen and nitrogen?')
            st.write('Possibly. If they exist oxygen and nitrogen would remain in the planets atmosphere.')
        else:
            st.write('No') 

        st.write('Does the planets sun have a suitable luminosity for the orbit of the planet?')
        if ((Selected_Planet['Orbital Radius'] > Selected_Planet['Lum_Min']) & (Selected_Planet['Orbital Radius'] < Selected_Planet['Lum_Max'])).all():
            st.write('Yes !')
        else:
            st.write('No') 

        st.write('Does the planet have a temperature between 258 K and 395 K?')
        if ((Selected_Planet['Equilibrium Temperature [K]'] > 258) & (Selected_Planet['Equilibrium Temperature [K]'] < 395)).all():
            st.write('Yes !')
            st.write('Is it possible the planet has water?')
            st.write('Possibly. If it exists water could be present in all three states of matter.')
        else:
            st.write('No')  
