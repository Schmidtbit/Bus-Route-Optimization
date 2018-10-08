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
    OUTPUT: List; List of Intersections within buffer distance of block
    '''
    block = blockGeo.buffer(400) # 400 meters is about 1/4 mile
    L = []
    for i in intersections:
        if i.intersects(block) == True:
            L.append(i)
    return L


def BlockList(IntersectionGeo, AoA_df, buffer=200):
    '''
     INPUT:  IntersectionGeo: Shapely Geometry Object
            blocks: Shapely Geometry Series of all blocks
            buffer: integer (in meters) of distance to search (200 = .024 mile -- approx)
     OUTPUT: List; List of Blocks within buffer distance of intersection
    '''
    blocks_df = AoA_df[['geometry', 'population']]
    intersection = IntersectionGeo.buffer(200) #search for all blocks within 200 meters (or about 0.124 miles)
    blockList = []
    iPop = 0 
    for row in range(blocks_df.shape[0]):
        geo = blocks_df.iloc[row]['geometry']
        pop = blocks_df.iloc[row]['population']
        if geo.intersects(intersection) == True:
            blockList.append(geo)
            iPop += pop
    
    return blockList , iPop
    

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

def BlocksPerIntersection(intersections_df, AoA_df):
    '''
    INPUT:  AoA_df: GeoDataFrame of Area of Interest
            intersections_df: GeoDataFrame of intersections 

    OUTPUT: intersections_df: GeoDataFrame with new columns added ('bList', 'iPop')
            ** bList is a list of blocks near each intersection
            ** iPop is a population count assigned to each intersection
    '''
    blockArray = []
    popArray = []
    for intersection in intersections_df.geometry:
        blockList, intersectionPop = BlockList(intersection, AoA_df)
        blockArray.append(blockList)
        popArray.append(intersectionPop)

    intersections_df['bList'] = blockArray
    intersections_df['iPop'] = popArray

    return intersections_df





