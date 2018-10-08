import pandas
import geopandas


def MakeStops(intersections_df, meters=800):
    '''
    INPUT: DataFrame returned from BlocksPerIntersection() function

    OUTPUT: DataFrame
    '''

    # Sort the DataFrme in order of descending population
    iPop_df = intersections_df[intersections_df.iPop > 0].sort_values('iPop', ascending=False)

    indexList = []
    served = [] # population served at each bus stop identified
    while iPop_df.shape[0] != 0:
        stop = iPop_df.geometry.values[0]
        idx = iPop_df.index.values[0]
        indexList.append(idx)
        # identify the exclusion zone
        zone = stop.buffer(meters) # 400 meters = approx 1/4 mile
        # reach is the sum of all populations in the exclusion zone
        reach = iPop_df[iPop_df.geometry.intersects(zone) == True].iPop.sum()
        served.append([idx, reach])
        #filter out any intersections within exclusion zone
        iPop_df = iPop_df[iPop_df.geometry.intersects(zone) == False]

    stops_df = intersections_df[intersections_df.index.isin(indexList)]

    # convert the 'served' array into a DataFrame
    served_df = pandas.DataFrame(data=served, columns=['idx','mergedPop'], dtype='int')
    served_df.set_index('idx', inplace=True)
    
    # Merge DataFrames
    stops_df = stops_df.merge(served_df, left_index=True, right_index=True)

    return stops_df
