import streamlit as st
import pandas as pd
import altair as alt
from vega_datasets import data

@st.cache
def load_data():
    stations = pd.read_csv("cali-stations.csv")
    weather = pd.read_csv("cali-weather.csv")
    return (stations, weather)



# load the data
st.title("California's 16 Different Climate Zones")
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
              color=alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3')),
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
    colourSel = scale=alt.Scale(scheme = 'set3')
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

##############################################################################
#move on to the correlation part
st.text("\n")
st.text("Let's now think about the corelations between climate factors.")
st.text("""Below is the matrix of Latitude, Longitude, Minimum temperature(F), Elevation(m),
Precipitation(inch) and Snowfall(inch)""")
st.text("\n")

# get the features needed for the matrix
features = ['Latitude','Longitude','Tmin',"Elevation","Snow","PRCP"]

# visualize the corrlation matrix based on selected climate zones
scatter2=alt.Chart(dfWeather[zone_membership2]).mark_circle(size=1).encode(
    x=alt.X(alt.repeat("column"),scale=alt.Scale(zero=False),type="quantitative"),
    y=alt.Y(alt.repeat("row"),scale=alt.Scale(zero=False),type="quantitative"),
    tooltip=['Climate Zone','Month', 'Day'],
    color='Season'
).properties(
    width=70,
    height=70
).repeat(
    row=features,
    column=features
)

#display the chart
st.altair_chart(scatter2)

##############################################################################
# move on to season multiselect interaction
st.text("\n")
st.text("""
It seems there are some correlation between latitude & minimum temperature,
elevation & minimum temperature and elevation & precipitation. Let's zoom into 
seasons for further exploration."""
)

# to get weather stations in selected seasons
seasons = dfWeather['Season'].sort_values(ascending=True)
seasons_multisel = st.multiselect("Please select/deselect seasons:", 
                               seasons.unique(), default=seasons.unique())
seasons_membership = get_season_membership(dfWeather, seasons_multisel)
st.text("(Autumn season data is missing from the orinigal datadet)")
st.text("\n")

# draw the correlation scatterplot and transform regression of latitude and tmax
scatter1=alt.Chart(dfWeather[seasons_membership]).mark_circle(size=2).encode(
    x=alt.X('Latitude',scale=alt.Scale(zero=False)),
    y=('Tmin'),
    color=alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3')),
    tooltip=['Climate Zone','Tmin','Latitude','Month', 'Day']
).properties(
    width=800,
    height=300
)
r1 = scatter1.transform_regression('Latitude', 'Tmin', method="poly", order=3).mark_line(color="red")
st.altair_chart(scatter1+r1)

# draw a histogram of latitude within a certain range of temperature
hist=alt.Chart(dfWeather[seasons_membership]).mark_bar(
    tooltip=True
).encode(
    x=alt.X('Latitude',bin=True),
    y=alt.Y(aggregate='count', type='quantitative'),
    tooltip=['Climate Zone','Latitude','Tmin','Month', 'Day']    
)

# add selection to the scatterplot and the histogram
selection= alt.selection_interval()
scatter1.add_selection(selection).encode(
    color=alt.condition(selection, alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3')), alt.value('grey'),type='ordinal')
).properties(
    width=300,
    height=200
) | hist.encode(
    alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3'))
).properties(
    width=300,
    height=200
).transform_filter(selection)

##############################################################################
# draw the correlation scatterplot and transform regression of elevation and tmax
scatter2=alt.Chart(dfWeather[seasons_membership]).mark_circle(size=2).encode(
    x=alt.X('Elevation',scale=alt.Scale(zero=False)),
    y=('Tmin'),
    color=alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3')),
    tooltip=['Climate Zone','Tmin','Elevation','Month', 'Day']
).properties(
    width=800,
    height=300
)
r2 = scatter2.transform_regression('Elevation', 'Tmin', method="poly", order=3).mark_line(color="red")
st.altair_chart(scatter2+r2)

# draw a histogram of elevation within a certain range of temperature
hist2=alt.Chart(dfWeather[seasons_membership]).mark_bar(
    tooltip=True
).encode(
    x=alt.X('Elevation',bin=True),
    y=alt.Y(aggregate='count', type='quantitative'),
    tooltip=['Climate Zone','Tmin','Elevation','Month', 'Day']    
)

# add selection to the scatterplot and the histogram
selection2= alt.selection_interval()
scatter2.add_selection(selection2).encode(
    color=alt.condition(selection2, alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3')), alt.value('grey'),type='ordinal')
).properties(
    width=300,
    height=200
) | hist2.encode(
    alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3'))
).properties(
    width=300,
    height=200
).transform_filter(selection2)


##############################################################################
# draw the correlation scatterplot and transform regression of elevation and precipitation
scatter4=alt.Chart(dfWeather[seasons_membership]).mark_circle(size=2).encode(
    x=alt.X('Elevation',scale=alt.Scale(zero=False)),
    y=alt.Y('PRCP',scale=alt.Scale(zero=False)),
    color=alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3')),
    tooltip=['Climate Zone','Elevation','PRCP','Month', 'Day']
).properties(
    width=800,
    height=300
)
r4 = scatter4.transform_regression('Elevation', 'PRCP', method="poly", order=3).mark_line(color="red")
st.altair_chart(scatter4+r4)

# draw a histogram of elevation within a certain range of precipitation
hist4=alt.Chart(dfWeather[seasons_membership]).mark_bar(
    tooltip=True
).encode(
    x=alt.X('Elevation',bin=True),
    y=alt.Y(aggregate='count', type='quantitative'),
    tooltip=['Climate Zone','Elevation','PRCP','Month', 'Day']        
)

# add selection to the scatterplot and the histogram
selection4= alt.selection_interval()
scatter4.add_selection(selection4).encode(
    color=alt.condition(selection4, alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3')), alt.value('grey'),type='ordinal')
).properties(
    width=300,
    height=200
) | hist4.encode(
    alt.Color('Climate Zone:O', scale=alt.Scale(scheme = 'set3'))
).properties(
    width=300,
    height=200
).transform_filter(selection4)
