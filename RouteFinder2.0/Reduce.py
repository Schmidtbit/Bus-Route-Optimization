import geopandas

def filterStops(CurrentStops_df, stops_df):
    goalNum = CurrentStops_df.shape[0]/2
    minPop = stops_df.mergedPop.min()
    maxPop = stops_df.mergedPop.max()
    for bench in range(minPop, maxPop):
        filterStops = stops_df[stops_df.mergedPop > bench]
        if filterStops.shape[0] <= goalNum:
            return filterStops, bench