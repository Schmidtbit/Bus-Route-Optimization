from geopandas import GeoSeries
from shapely.ops import cascaded_union
import matplotlib.pyplot as plt

def makeBoundary(df):
    # create a list of geometries
    polygons = []
    for geo in df[['geometry']].values:
        polygons.append(geo[0])

    boundary = GeoSeries(cascaded_union(polygons))
    #boundary.plot(color='white', edgecolor='k')
    #plt.show()

    return boundary
