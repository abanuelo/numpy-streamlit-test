import pandas as pd
import plotly.express as px
import streamlit as st

# Set Mapbox token
# px.set_mapbox_access_token("YOUR_MAPBOX_ACCESS_TOKEN")

# Display title and text
st.title("Week 1 - Data and visualization")
st.markdown("Here we can see the dataframe created during this week's project.")

# Read dataframe
dataframe = pd.read_csv(
    "WK1_Airbnb_Amsterdam_listings_proj_solution.csv",
    names=[
        "Airbnb Listing ID",
        "Price",
        "Latitude",
        "Longitude",
        "Meters from chosen location",
        "Location",
    ],
    skiprows=1  # skip the header row if your CSV has one
)

# We have a limited budget, therefore we would like to exclude
# listings with a price above 100 pounds per night
dataframe = dataframe[dataframe["Price"].str.replace("£ ", "").astype(float) <= 100]

# Display as integer
dataframe["Airbnb Listing ID"] = dataframe["Airbnb Listing ID"].astype(int)
# Round off values
dataframe["Price"] = "£ " + dataframe["Price"].str.replace("£ ", "").astype(float).round(2).astype(str)
# Rename the number to a string
dataframe["Location"] = dataframe["Location"].replace(
    {1.0: "To visit", 0.0: "Airbnb listing"}
)

# Display dataframe and text
st.dataframe(dataframe)
st.markdown("Below is a map showing all the Airbnb listings with a red dot and the location we've chosen with a blue dot.")

# Create the plotly express figure
fig = px.scatter_mapbox(
    dataframe,
    lat="Latitude",
    lon="Longitude",
    color="Location",
    color_discrete_sequence=["blue", "red"],
    zoom=11,
    height=500,
    hover_name="Price",
    hover_data=["Meters from chosen location", "Location"],
    labels={"color": "Locations"},
)

# Center the map
fig.update_layout(mapbox=dict(center=dict(lat=dataframe["Latitude"].mean(), lon=dataframe["Longitude"].mean())))

# Set the map style
fig.update_layout(mapbox_style="stamen-terrain")

# Show the figure
st.plotly_chart(fig, use_container_width=True)
