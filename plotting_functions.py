#------------------------------#
# IMPORT LIBRARIES
#------------------------------#

import geopandas as gpd
from geopandas import GeoSeries
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from shapely.geometry import Point, Polygon
from shapely.geometry import LineString, shape

#------------------------------#
# PLOTTING FUNCTIONS
#------------------------------#


def plot_roads(streets_df, secondary_df):
    '''
    INPUT:  streets_df = GeoDataFrame of local roads made with local_roads() function
            secondary_df = GeoDatFrame of secondary roads made with local_roads() function

    OUTPUT: plot of road network
    '''
    fig, ax = plt.subplots(figsize=(10,10))
    streets_df.plot(ax=ax, color='grey', linewidth=.2, markersize=.2, label='local roads')
    secondary_df.plot(ax=ax, color='green', linewidth=1, markersize=.2, label='secondary roads' )
    ax.set_title('Local Road Netork')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(fontsize=12, markerscale=10)
    ax.set_aspect('equal')

    plt.show()



def block_data_viz(cleaned_geo_df):
    '''
    INPUT:  GeoDatFrame cleaned with clean_census_data() function

    OUTPUT: census data visualizations
    '''

    fig, (ax1, ax2) = plt.subplots(2,1,figsize=(10,10))

    pop_density = cleaned_geo_df.pop_per_sq_mi
    pop_density.hist(ax=ax1, bins=250, range=(1,80000))
    ax1.set_title('Population Density per Census Block')
    ax1.set_xlabel('People per Square Mile')
    ax1.set_ylabel('Frequency')
    ax1.set_yscale('log')

    block_areas = cleaned_geo_df.area_sq_miles
    block_areas.hist(ax=ax2, bins=250, range=(0,.5))
    ax2.set_title('Block Area Distribution')
    ax2.set_xlabel('Square Miles per Census Block')
    ax2.set_ylabel('Frequency')
    ax2.set_yscale('log')

    plt.show


def pop_heatmap(cleaned_geo_df):
    '''
    INPUT:  GeoDatFrame cleaned with clean_census_data() function

    OUTPUT: population density heat map by city census block
    '''
    fig, ax = plt.subplots(1,1,figsize=(10,10))
    cleaned_geo_df.plot(ax=ax, column='pop_per_sq_mi', cmap='Oranges', edgecolor='black', scheme='Quantiles', linewidth=.1)
    ax.set_title('Austin Population Density Heat Map')
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()



def plot_stops(stops_df, clusters_df, roads_df):
    '''
    INPUT:  stops_df: GeoDataFrame of current bus stops cleaned with current_bus_system() function
            clusters_df: GeoDataFrame of population clusters generated with make_clusters() function
    OUTPUT: plot of curent bus stop vs. population cluster centers
    '''
    n = stops_df.shape[0]
    k = clusters_df.shape[0]

    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(20,10), sharey=True)

    roads_df.plot(ax=ax1, color='black', linewidth=.15)
    stops_df.plot(ax=ax1, marker='.', color='red', markersize=1)
    ax1.set_title('{} Curent Bus Stops'.format(n))
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax1.set_aspect('equal')

    roads_df.plot(ax=ax2, color='black', linewidth=.15)
    clusters_df.plot(ax=ax2, marker='.', color='red', markersize=1)
    ax2.set_title('{} Population Cluster Centers'.format(k))
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_aspect('equal')

    plt.subplots_adjust(wspace=.05)
    plt.show()


def plot_tracts(city_tracts_df):
    '''
    INPUT: city_tracts_df; GeoDataFrame cleaned with make_tract_geos() function
    OUTPUT: GeoDataFrame of census tract shape objects
    '''
    fig, ax = plt.subplots(figsize=(10,10))
    ax.set_aspect('equal')
    city_tracts_df.geometry.plot(ax=ax, alpha=.1, edgecolor='blue')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
