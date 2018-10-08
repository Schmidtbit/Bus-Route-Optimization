import geopandas

def Population(stops_df, AoA_df):
    '''
    INPUT:
    
    OUTPUT:
    '''
    population = 0
    # iterate through stops
    while stops_df.shape[0] != 0:
        stop = stops_df.geometry.values[0]
        # Define are within 400 meters of stop
        buffer400 = stop.buffer(400)
        # filter blocks in buffer range
        blocks_df = AoA_df[AoA_df.geometry.intersects(buffer400) == True]
        # Find fractional area of buffer over block
        blocks_df['fractionalArea'] = blocks_df.geometry.intersection(buffer400).area / blocks_df.geometry.area
        # Find fractional population
        blocks_df['fractionalPop'] = blocks_df.population * blocks_df.fractionalArea
        # Add population
        population += blocks_df.fractionalPop.sum()
        # Filter CurrentStops_df to reduce population duplicates
        buffer200 = stop.buffer(200)
        stops_df = stops_df[stops_df.geometry.intersects(buffer200) == False]
    
    return int(population)
    
        
