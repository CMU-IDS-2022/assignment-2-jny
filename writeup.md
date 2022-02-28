# Project name

![A screenshot of your application. Could be a GIF.](screenshot.png)

TODO: Update screenshot

TODO: Short abstract describing the main goals and how you achieved them.
Using NOAA Daily Historical Climatology Network 2017 dataset of daily weather, this app focus on the daily and seasonal climate trends in 16 California climate zones. The first section mappes the geology and the bigger picture of temperature sort by climate zones and elevtation.  The second section focuses on the correlation inbetween major climate factors where seasonal trends can be visualized.  

## Project Goals

TODO: **A clear description of the goals of your project.** Describe the question that you are enabling a user to answer. The question should be compelling and the solution should be focused on helping users achieve their goals. 

California is a large state that spans both east-west and north-south. As a result, California has 16 different climate zones under the building code. When designing the built environment, it is crucial to design based on the local climate to ensure the comfort of the people in that environment. Architects, engineers, and developers must not ignore the differences in the climate and treat California as one climate zone. Therefore, this Streamlit app is an exploration to investigate the question of: **What are the differences amongst the 16 different climate zones?** This guiding question will help us explore the trends that distinguish each climate zone, and which variables are correlated with each other that helps to identify a climate zone.

The data used in this Streamlit app study is from the 2017 dataset of daily weather in the US provided by the NOAA Daily Global Historial Climatology Network.

## Design

TODO: **A rationale for your design decisions.** How did you choose your particular visual encodings and interaction techniques? What alternatives did you consider and how did you arrive at your ultimate choices?

This exploration focused on two types of visual encodings to best help us answer our guiding question. In the first section of this Streamlit app, we focused on the visualising the bigger picture, particularly through the use of maps with location-based information layered on top. This visualisation method is useful to understand how location (latitude and longitude) plays a role in the weather/climate. Aside from maps, we also used a chart to visualise the full set of data for the entire 2017 year. 

In the second section of this study, we focus on scatterplots and histograms to find possible correlation between 6 climate factors: latitude, longtitude, precipitation, snowfall, elevation and minimun temperature. We start by plotting a matrix and find out 3 most obvious correalations: latitude & minimum temperature, elevation & temperature and elevation & precipitation. We can filter by seasons in this section although the autumn season data is missing. Then we display a larger scatterplot with a polyline regression summarizing the correlation and create a multiselect interaction between the scatterplot and histogram identifying climate stations within selection.

## Development

TODO: **An overview of your development process.** Describe how the work was split among the team members. Include a commentary on the development process, including answers to the following questions: Roughly how much time did you spend developing your application (in people-hours)? What aspects took the most time?

Before splitting any work, we met together to discuss which dataset to use, what our goals are, and what questions we are interested in focusing on. After an initial look through the weather dataset, we discussed ways we can visualise the data and concluded with the two types of visual encodings as mentioned above. The first section about the big picture visualisations (maps and annual chart) was completed by Jamie Ho. The second section about the more detailed analysis on climate factor correlations (matrix, scatterplot and histograms) was completed by Yi Zhou. 

In addition to the data visualisation, adding Climate Zones to the dataset and cleaning the data was necessary. The following actions were done on the weather dataset provided by the NOAA Daily Global Historial Climatology Network:
  - Filter for only the data in the state of California
  - Remove fields that we decided not to focus on (Average temperature, Fastest wind speed)
  - Replace any missing data in the Tmin and Tmax columns with 0
  - Add additional field of Climate Zone (based on https://caenergy.maps.arcgis.com/apps/webappviewer/index.html?id=5cfefd9798214bea91cc4fddaa7e643f)

## Success Story

TODO:  **A success story of your project.** Describe an insight or discovery you gain with your application that relates to the goals of your project.
