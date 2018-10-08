import geopandas


def CurrentStops(file_path, shape_obj, crs):
    '''
    INPUT:  file_path: str; path to current city bus stop shapefile data
            shape_obj: shapely.geometry.Polygon Object
    OUTPUT: bus_stop GeoDataFrame
    '''
    stops_df = geopandas.read_file(file_path)
    stops_df.to_crs(crs, inplace=True)
    stops_df = stops_df[stops_df.geometry.within(shape_obj)]
    
    return stops_df
