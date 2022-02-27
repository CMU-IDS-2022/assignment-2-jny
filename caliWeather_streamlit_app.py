import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

@st.cache
def load_data():
    stations = pd.read_csv("data\cali-stations.csv")
    weather = pd.read_csv("data\cali-weather.csv")
    return (stations, weather)



# load the data
st.title("The Differences of Weather and Climate in California")
with st.spinner(text="Loading data..."):
    dfStations, dfWeather = load_data()
    # dfStations
    # dfWeather
st.text("Jamie Ho & Yi Zhou")
st.text("""California is a large state that spans east-west and north-south. 
As a result, California has 16 different climate zones under the building code.
When designing the built environment, it is crucial to design for the local climate
to ensure the comfort of the people in that environment.
This Streamlit app is an exploration to investigate the question of: 
\"What parameters are used to distinguish amongst the 16 different climate zones?\"""")
st.text("\n")

# get additional map data to visualise
counties = alt.topo_feature(data.us_10m.url, 'counties')
states = alt.topo_feature(data.us_10m.url, 'states')

# setup to display the counties in the state of California
cali_map =(
    alt.Chart(data = counties)
    .mark_geoshape(
        fill='#F0F0F0',
        stroke = 'black',
        strokeWidth = 0.1
    )
    .transform_calculate(state_id = "(datum.id / 1000)|0")
    .transform_filter((alt.datum.state_id)==6)
)

# boolean function for weather stations that are in selected climate zones
@st.cache
def get_zone_membership(df, climateZones):
    labels = pd.Series([1] * len(dfStations), index=dfStations.index)
    if climateZones:
        labels &= dfStations['Climate Zone'].isin(climateZones)
    return labels

@st.cache
def get_zone_membership2(df, climateZones):
    labels = pd.Series([1] * len(dfWeather), index=dfWeather.index)
    if climateZones:
        labels &= dfWeather['Climate Zone'].isin(climateZones)
    return labels

# boolean function for data that is in the selected season
@st.cache
def get_season_membership(df, season):
    labels = pd.Series([1] * len(dfWeather), index=dfWeather.index)
    if season:
        labels &= dfWeather['Season'].isin(season)
    return labels

# to get weather stations in selected climate zones
zones = dfStations['Climate Zone'].sort_values(ascending=True)
zone_multisel = st.multiselect("Please select/deselect climate zones:", 
                               zones.unique(), default=zones.unique())
zone_membership = get_zone_membership(dfStations, zone_multisel)

# setup to display weather stations as points
stations_map = (
    alt.Chart(dfStations[zone_membership]).mark_point().encode(
              latitude='Latitude',
              longitude='Longitude',
              color=alt.Color('Climate Zone:O', scale=alt.
                              Scale(scheme = 'dark2')),
              tooltip=['Station', 'Latitude', 'Longitude', 'Elevation', 
                       'Climate Zone']
    )
).properties(
    width=325, height=350
)

# setup to display weather stations as points
elevation_map = (
    alt.Chart(dfStations[zone_membership]).mark_point().encode(
              latitude='Latitude',
              longitude='Longitude',
              color=alt.Color('Elevation'),
              tooltip=['Station', 'Latitude', 'Longitude', 'Elevation', 
                       'Climate Zone']
    )
).properties(
    width=325, height=350
)

# display the charts
st.text("\n")
st.text("Climate Zone and Elevation (in meters) of the Weather Stations")
st.altair_chart((cali_map + stations_map) | (cali_map + elevation_map))

##############################################################################
# CHART WITH DATE AND TEMPERATURE
st.text("\n")
displayBy = st.selectbox(
    'Please select how you would like to display the min/max temperature',
    ('Climate Zone', 'Elevation')
)

# to get weather stations in selected climate zones
zones2 = dfStations['Climate Zone'].sort_values(ascending=True)
zone_membership2 = get_zone_membership2(dfWeather, zone_multisel)

# Logic for colour coding the graph 
if displayBy == 'Climate Zone':
    colourSel = 'Climate Zone:O'
else:
    colourSel = 'Elevation'

# Select the time frame
interval = alt.selection_interval(encodings=['x'])

# Setup and display of the two charts
st.text("\n")
st.text("Annual Min and Max Temperature (F)")
largeChart = alt.Chart(dfWeather[zone_membership2]).mark_point(size=1).encode(
    x='LongDate:T', y='Tmin:Q', y2='Tmax:Q', color= colourSel,
    tooltip=['Station', 'Climate Zone', 'Tmin', 'Tmax', 
            'Month', 'Day', 'Season']
)
chart = largeChart.encode(
    x=alt.X('LongDate:T', scale=alt.Scale(domain=interval.ref()))
    ).properties(
        width=700, height=300
)
view = largeChart.add_selection(
    interval
).properties(
    width=700, height=50
)
st.altair_chart(chart & view)




