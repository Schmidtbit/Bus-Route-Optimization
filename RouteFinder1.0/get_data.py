#------------------------------#
# IMPORT LIBRARIES
#------------------------------#

import geopandas as gpd
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from shapely.geometry import Point, Polygon

#------------------------------#
# FUNCTIONS
#------------------------------#

def define_city_geo(file_path, city_name):
    '''
    INPUT:  file_path = string; path to state level census boundary shapefile (i.e. 'gz_2010_48_160_00_500k.shp')
            city_name = string; name of census place of interest (i.e. 'Austin')

    OUTPUT: 1) shapely.geometry.multipolygon.MultiPolygon Object
            2) geopandas.geodataframe.GeoDataFrame
    '''
    # Read in file to GeoPandas
    geo_df = gpd.read_file(file_path)
    # Filter NAME
    geo_df = geo_df[geo_df.NAME == city_name]
    # Convert crs to EPSG: 4326 (GPS) and define geometry
    geo_df.to_crs({'init': 'epsg:4326'}, inplace=True)

    geo_shape = geo_df.geometry.values[0]

    return geo_shape , geo_df

def clean_census_data(file_path, county_number, shape_obj):
    '''
    INPUT:  file_path = string; path to state level census block shapefile data (i.e. 'tabblock2010_48_pophu.shp')
            county_number = str; census designated number for county of interest (i.e. '453' for Austin)
            shape_obj = shapely.geometry.Polygon Object

    OUTPUT: GeoDataFrame of city level census blocks
    '''

    # Read in file to GeoPandas
    state_df = gpd.read_file(file_path)
    # Filter to county level
    county_df = state_df[state_df.COUNTYFP10 == county_number]
    # Filter for city level
    county_df['in_city'] = county_df.geometry.within(shape_obj)
    city_df = county_df[county_df.in_city == True]

    # Convert crs to EPSG: 4326 (GPS) and define geometry
    city_df.to_crs({'init': 'epsg:4326'}, inplace=True)
    # Define block-level centroids
    city_df['centroids'] = city_df.geometry.centroid

    # Make a geometry column with geometry in UTM13N (EPSG:26913) units
    city_df['UTM13N'] = city_df.geometry.to_crs(epsg=26913)
    city_df.set_geometry('UTM13N', inplace=True)
    # Calculate block Area in square miles
    sq_meter_sq_miles_multiplier = 0.000000386102
    city_df['area_sq_miles'] = city_df['UTM13N'].area*sq_meter_sq_miles_multiplier
    # Calculate population density per census block
    city_df['pop_per_sq_mi'] = city_df.POP10/city_df.area_sq_miles
    # Calculate Housing Density per census plock
    city_df['housing_density_sq_mile'] = city_df.HOUSING10/city_df.area_sq_miles

    # Convert crs back to EPSG: 4326 (GPS) and define geometry
    city_df.to_crs({'init': 'epsg:4326'}, inplace=True)
    city_df.set_geometry('geometry')
    city_df.drop(columns=['in_city', 'UTM13N','STATEFP10','COUNTYFP10'], inplace=True)

    centroids_df = city_df.drop(columns=['geometry'])
    centroids_df.set_geometry('centroids', inplace=True)
    centroids_df.to_crs({'init': 'epsg:4326'}, inplace=True)

    blocks_df = city_df.drop(columns=['centroids'])
    blocks_df.set_geometry('geometry', inplace=True)
    blocks_df.to_crs({'init': 'epsg:4326'}, inplace=True)

    return centroids_df, blocks_df

def make_tract_geos(file_path, county_code, shape_obj):
    '''
    INPUT:  file_path: str: path to tracts shapefile data
            county_code:  str; census designated county code (i.e. '453' for Austin)
            shape_obj: shape_obj = shapely.geometry.Polygon Object
    OUTPUT: GeoDataFrame of census tract shape objects
    '''
    tracts_df = gpd.read_file(file_path)
    county_tracts = tracts_df[tracts_df.COUNTY == county_code]
    tracts_df.to_crs({'init': 'epsg:4326'}, inplace=True)
    county_tracts['in_city'] = county_tracts.geometry.intersects(shape_obj)
    city_tracts = county_tracts[county_tracts.in_city == True]
    city_tracts['geometry'] = city_tracts.geometry.intersection(shape_obj)

    return city_tracts

def current_bus_system(file_path, shape_obj):
    '''
    INPUT:  file_path: str; path to current city bus stop shapefile data
            shape_obj: shapely.geometry.Polygon Object
    OUTPUT: bus_stop GeoDataFrame
    '''
    stops_df = gpd.read_file(file_path)
    stops_df.to_crs({'init': 'epsg:4326'}, inplace=True)
    stops_df = stops_df[stops_df.geometry.within(shape_obj)]
    return stops_df

def local_roads(file_path, shape_obj):
    '''
    INPUT:  file_path = string; path to county level census roads shapefile (i.e. 'tl_2017_48453_roads.shp')
            shape_obj = shapely.geometry.Polygon Object

    OUTPUT: 1) street level GeoDataFrame of local roads
            2) secondary level GeoDataFrame of local roads
    '''
    # Read in file to GeoPandas
    roads_df = gpd.read_file(file_path)
    # Filter Relavent Roads
    # S1400 = Local Neighborhood Road, Rural Road, City Street
    # S1200 = Secondary Road (U.S. Highway, State Highway or County Highway system)
    roads_df = roads_df[roads_df.MTFCC.isin(['S1400','S1200'])]
    # Convert crs to EPSG: 4326 (GPS) and define geometry
    roads_df.to_crs({'init': 'epsg:4326'}, inplace=True)
    # Filter for roads inside city limits
    roads_df['in_boundary'] = roads_df.geometry.intersects(shape_obj)
    local_roads = roads_df[roads_df['in_boundary'] == True]
    # Clip roads
    local_roads['geometry'] = local_roads.geometry.intersection(shape_obj)
    # Get rid of Point Objects
    local_roads['length'] = local_roads.geometry.length
    local_roads = local_roads[local_roads.length != 0]
    # Divide dataFrame into streets and secondary roads
    streets_df = local_roads[local_roads.MTFCC == 'S1400']
    secondary_df = local_roads[local_roads.MTFCC == 'S1200']

    return streets_df, secondary_df

if __name__ == '__main__':
    pass

    #boundary_path = 'data/boundary/gz_2010_48_160_00_500k.shp'
    #city_shape , city_df = define_city_geo(boundary_path, 'Austin')

    #census_block_path = '../population/tabblock2010_48_pophu.shp'
    #austin_centroids, austin_blocks = clean_census_data(census_block_path, '453', city_shape)

    # Save shapefiles
    #austin_centroids.to_file('data/austin_centroids_df/austin_centroids_df.shp', driver='ESRI Shapefile')
    #austin_blocks.to_file('data/austin_blocks_df/austin_blocks_df.shp', driver='ESRI Shapefile')
