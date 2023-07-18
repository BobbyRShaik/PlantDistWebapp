#!/usr/bin/env python
# coding: utf-8

# In[91]:


import ee
import geemap
import ipywidgets as widgets
import pandas as pd
import os
from ipyleaflet import ImageOverlay

# Initialize the Earth Engine Python API
ee.Initialize()

# Create a dropdown widget for selecting months
months_dropdown = widgets.Dropdown(options=['2019-01-01', '2019-03-01', '2019-05-01', '2019-07-01', '2019-09-01', '2019-11-01', '2019-12-31'], description='Select Month')

# Create the map
Map = geemap.Map(center=[5, 130], zoom=4, height="500px")

# Load the image collection
dataset = ee.ImageCollection('BIOPAMA/GlobalOilPalm/v1')

# Select the classification band
opClass = dataset.select('classification')

# Define visualization parameters
classificationVis = {'min': 1, 'max': 3, 'palette': ['ef00ff', 'ff0000', '696969']}

# Add the initial data to the map (default month: '2019-01-01')
Map.addLayer(opClass, classificationVis, 'Global Palm Oil Plantations 2019')

# Define a function to update the displayed data based on the selected month
def update_map(change):
    month = change['new']
    
    start_date = ee.Date(month)
    end_date = start_date.advance(1, 'month')
    filtered_dataset = opClass.filter(ee.Filter.date(start_date, end_date))
    filtered_dataset = filtered_dataset.select('classification')
    
    # Add the filtered data to the map
    Map.addLayer(filtered_dataset, classificationVis, 'Palm Oil Plantations')

# Call the update_map function when the dropdown value changes
months_dropdown.observe(update_map, 'value')

legend_dict = {
    'Industrial closed-canopy oil palm plantations': 'ff0000',
    'Other land covers and/or uses that are not closed-canopy oil palm': '696969',
    'Smallholder closed-canopy oil palm plantations': 'ef00ff'
}
Map.add_legend(legend_title="Plantation Types", legend_dict=legend_dict)

# Create a play button widget for animation
play_button = widgets.Play(min=0, max=len(months_dropdown.options) - 1, step=1, description="Play", interval=500)

# Link the play button to the dropdown
widgets.jslink((play_button, 'value'), (months_dropdown, 'index'))

def show_metadata(button):
    # Retrieve metadata for the image collection
    collection_info = dataset.getInfo()
    print('Type: ' + str(collection_info['type']))
    print('ID: ' + str(collection_info['id']))
    print('Version: ' + str(collection_info['version']))
    print('Keywords: ' + str(collection_info['properties']['keywords']))
    print('Thumb: ' + str(collection_info['properties']['thumb']))
    
# Function to download the map image directly
def display_bounds(button):
    # Define the file path for the downloaded image
    # Get the map's bounds
    bounds = Map.bounds
    
    print(bounds)

# Create a button to download the map image directly
display_bounds_button = widgets.Button(description="Display Map Bounds")
display_bounds_button.on_click(display_bounds)

def update_map_center(change):
    try:
        lat = float(lat_input.value)
        lon = float(lon_input.value)
        Map.center = [lat, lon]
    except ValueError:
        print("Invalid input. Please enter valid numeric values for latitude and longitude.")

# Create input widgets for latitude and longitude
lat_input = widgets.FloatText(value=Map.center[0], description='Latitude:')
lon_input = widgets.FloatText(value=Map.center[1], description='Longitude:')

# Call the update_map_center function when the user changes the input value
lat_input.observe(update_map_center, 'value')
lon_input.observe(update_map_center, 'value')

# Create a VBox layout to stack the input widgets and the map
input_box = widgets.VBox([lat_input, lon_input])

# Create a button to display metadata
metadata_button = widgets.Button(description="Show Metadata")

# Attach the show_metadata function to the button's click event
metadata_button.on_click(show_metadata)

# Get the first 7 images from the collection
first_7_images = ee.ImageCollection(dataset.limit(7).toList(7))
months = ['2019-01-01', '2019-03-01', '2019-05-01', '2019-07-01', '2019-09-01', '2019-11-01', '2019-12-31']

Map.ts_inspector(left_ts=first_7_images, right_ts=first_7_images, left_names=months, right_names=months)
Map

# Create an output widget to display the map
output_widget = widgets.Output()

# Display the map inside the output widget
with output_widget:
    display(Map)

# Create a VBox layout to stack the dropdown and map output vertically
layout = widgets.VBox([months_dropdown, play_button, metadata_button, display_bounds_button, input_box, output_widget])

# Display the layout
display(layout)


# In[ ]:





# In[ ]:




