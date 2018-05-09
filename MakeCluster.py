#------------------------------#
# IMPORT LIBRARIES
#------------------------------#

import geopandas as gpd
from geopandas import GeoSeries
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from sklearn.cluster import KMeans
from shapely.geometry import Point, Polygon
from shapely.geometry import LineString, shape
from shapely.prepared import prep



class MakeClusters:
    def __init__(self,centroids_geo_df, streets_df):
        '''
        INPUT:  centroids_geo_df = centroids GeoDatFrame returned from clean_census_data() function
                streets_df =
        '''
        self.centroids_geo_df = centroids_geo_df
        self.streets_df = streets_df
        self.n_clusters = None
        self.random_state = 0
        self.clusters_df = None
        self.model = None


    def fit(self, n_clusters):
        self.n_clusters = n_clusters
        #extracy coordinates from df
        self.centroids_geo_df.set_geometry('centroids', inplace=True)
        x = self.centroids_geo_df.geometry.x.values
        y = self.centroids_geo_df.geometry.y.values
        lat_long = [[x[i],y[i]] for i in range(x.shape[0])]


        # Perform KMeans Clustering
        self.model = KMeans(n_clusters=self.n_clusters, random_state=self.random_state)
        self.model.fit(lat_long)

        # Make Clusters df
        clusters = [Point(x[0],x[1]) for x in self.model.cluster_centers_]
        clusters_df = pd.DataFrame(clusters)
        clusters_df.columns = ['cluster_pts']
        self.clusters_df = gpd.GeoDataFrame(clusters_df, crs = {'init': 'epsg:4326'}, geometry='cluster_pts')


    def snap_one(self, point, rad=0):
        '''
        This function searches a radius around a centroid to find nearest
        roads. Then finds the road with the minimum distance to the centroid and returns
        the coordinates of that location on the road.

        INPUT:  point = Point Object returned from make_clusters() function
                rad = initial search radius

        OUTPUT: new_point
        '''
        # 1. Start with an empty list of roads
        line_list = []
        # 2. Search for closest roads to the point
        while line_list == []:
            #Define search radius
            rad = rad + .01
            search_radius = point.buffer(rad)
            #Prepare my search radius
            prep_radius = prep(search_radius)
            #Make a list of near-by objects
            hit_list = list(filter(prep_radius.contains, self.streets_df.geometry.values))
            #Filter the list of objects to only include roads (not other point objects)
            line_list = [item for item in hit_list if shape(item).geom_type == 'LineString']


        # 3. Select nearest road to point
        road = None
        value = None
        for rd in line_list:
            val = rd.distance(point)
            if road == None:
                road = rd
                value = val
            if val < value:
                road = rd
                value = val
            else:
                continue

        # 4. Use linear referencing method to return a new point object
        dist = road.project(point)
        new_pt = road.interpolate(dist)

        return new_pt

    def snap(self):
        #modifiy clusters_df with new point coordinates snapped to road network
        streets = self.streets_df.geometry.values
        clusters = self.clusters_df.geometry.values
        self.clusters_df['new_geometry'] = [self.snap_one(pt) for pt in clusters]
        self.clusters_df.set_geometry('new_geometry', inplace=True)
