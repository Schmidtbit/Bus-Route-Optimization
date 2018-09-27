import geopandas 

def joinDFs(path_blockGEOs, df):
    '''
    INPUT:  (1) string; path to blockGEOs 
            (2) DataFrame returned by 'makeAPI_PopByBlock2010' 
    
    OUTPUT: DataFrame
    '''
    
    # create a geo-pandas DataFrame and filter the columns for only ID and 'geometry'
    geo_df = geopandas.read_file(path_blockGEOs)
    geo_df = geo_df[['GEOID10','geometry']]
    geo_df.set_index('GEOID10', inplace=True)
    
       
    # join the tiger_df and the df tables
    joined_df = geo_df.join(df, how='right')
    
 
    print('GeoDataFrame with projection = {}'.format(joined_df.crs))
    
    return joined_df

