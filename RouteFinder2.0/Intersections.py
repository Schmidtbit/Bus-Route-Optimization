import osmnx as ox
import matplotlib.pyplot as plt

def getIntersections(boundary, projection, tolerance=100):
    '''
    INPUT:  boundary shap
            projection in UTM
            int (in meters) representing tolerance of clean_intersections() function for osmnx package

    OUTPUT: GeoSeries of Intersections
    '''

    # Create Graph
    G = ox.graph_from_polygon(boundary, network_type='drive')
    ox.plot_graph(G)
    plt.show()

    # Clean Intersections
    G_proj = ox.project_graph(G, to_crs=projection)
    intersections = ox.clean_intersections(G_proj, tolerance=tolerance, dead_ends=False)

    return intersections


def IntersectionList(blockGeo, intersections, buffer=400):
    '''
    INPUT:  blockGeo: Shapely Geometry Object
            intersections: Shapely Geometry Series from getIntersections() function
            buffer: integer (in meters) of distance to search (400 = 1/4 mile -- approx)
    OUTPUT: List; List of Intersection for given blockGeo
    '''
    block = blockGeo.buffer(400) # 400 meters is about 1/4 mile
    L = []
    for i in intersections:
        if i.intersects(block) == True:
            L.append(i)
    return L



def IntersectionsPerBlock(AoA_df, intersections):
    '''
    INPUT:  AoA_df: GeoDataFrame of Area of Interest
            intersections: GeoSeries of intersections from getIntersections()

    OUTPUT: AoA_df: GeoDataFrame with new columns added ('iList', 'iCounts')
            ** iList is a list of intersections near each block
            ** iCount is a count of intersections near each block
    '''
    iArray = []
    iCounts = []
    for block in AoA_df.geometry:
        iList = IntersectionList(block, intersections)
        iArray.append(iList)
        iCounts.append(len(iList))

    AoA_df['iList'] = iArray
    AoA_df['iCounts'] = iCounts

    AoA_underserved = AoA_df[(AoA_df.iCounts == 0) & (AoA_df.population != 0)]

    underserved = sum(AoA_underserved.population)
    print('{} people do not live near an intersection'.format(underserved))
    return AoA_df
