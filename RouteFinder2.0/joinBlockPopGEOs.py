import geopandas as geo_pd

def joinDFs(path_blockGEOs, df):
    '''
    INPUT:  (1) string; path to blockGEOs 
            (2) DataFrame returned by 'makeAPI_PopByBlock2010' 
    
    OUTPUT: DataFrame
    '''
    
    # create a geo-pandas DataFrame and filter the columns for only ID and 'geometry'
    geo_df = geo_pd.read_file(path_blockGEOs)
    geo_df = geo_df[['GEOID10','geometry']]
    print(geo_df.crs)
    # Set Index
    geo_df.set_index('GEOID10', inplace=True)
  
    # join the tiger_df and the pop_df tables
    joined_df = df.join(geo_df, on='ID')
    
    return joined_df

