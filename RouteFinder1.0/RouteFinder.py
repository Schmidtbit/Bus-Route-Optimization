#------------------------------#
# IMPORT LIBRARIES
#------------------------------#

import geopandas as gpd
from geopandas import GeoSeries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from sklearn.cluster import KMeans
from shapely.geometry import Point, Polygon, box
from shapely.geometry import LineString, shape
from shapely.prepared import prep
import random
from get_data import local_roads

#----------------------------------------#
# ROUTE DISCOVERY GENETIC ALGORITHM CLASS
#----------------------------------------#


class RouteFinder:
    def __init__(self):
        '''
        INPUT: bus_stops = list of shapely point objects
        '''
        self.bus_stops = None
        self.bus_stops_geo = None
        self.minx = None
        self.maxx = None
        self.miny = None
        self.maxy = None
        self.roads = None
        self.region = None
        self.N = None
        self.station = None
        self.routes_dict = None
        self.end_a_key = None
        self.end_b_key = None
        self.route_list = None

    def evaluation_area(self, tract_list, zone_name, tracts_df, stops_df, file_path):
        '''
        INPUT:  zone_name = str; string to name the zone
                tract_list = list of strings; list of census tracts to evaluate
                tracts_df = GeoDataFrame returned from make_tract_geos() function
                stops_df = GeoDataFrame returned from snap_all() function
                file_path = str; path to roads shapefile
        '''
        # Create boundary shape of evaluation zone
        zone_df = tracts_df[tracts_df.TRACT.isin(tract_list)]
        for row in range(zone_df.shape[0]-1):
            if row == 0:
                current = zone_df.geometry.values[row]
            else:
                current = boundary_poly
            next_ = zone_df.geometry.values[row+1]
            boundary_poly = current.union(next_)
        boundary_poly = GeoSeries(boundary_poly)
        boundary_poly.crs = {'init': 'epsg:4326'}
        self.region = boundary_poly

        # Identify stops inside the evaluation zone
        stops_df['in_zone'] = stops_df.geometry.intersects(self.region[0])
        self.bus_stops = stops_df[stops_df.in_zone == True].geometry.values
        self.bus_stops_geo = self.transform_to_GeoDataFrame(self.bus_stops)

        # Define Boundary Box
        self.minx = self.region.bounds.minx.values[0]
        self.maxx = self.region.bounds.maxx.values[0]
        self.miny = self.region.bounds.miny.values[0]
        self.maxy = self.region.bounds.maxy.values[0]

        # Identify roads inside the boundary box
        road_box = box(self.minx, self.miny, self.maxx, self.maxy)
        self.roads = local_roads(file_path, road_box)[0]




    def fit(self, start_pt, end_a, end_b, epochs, N=4):
        '''
        INPUT: start_pt = shapely point object (the area's main transfer station)
               end_a = shapely point object
               end_b = shapely point object
               epochs = integer
        '''
        #-------------------------------------------------#
        # Make a Dictionary of Stop ID's and Stop Locations
        #-------------------------------------------------#
        e = enumerate(self.bus_stops)
        stops_dict = {'start':start_pt}
        for idx, stop in e:
            if stop.x == end_a.x and stop.y == end_a.y:
                stops_dict[idx] = stop
                self.end_a_key = idx
            if stop.x == end_b.x and stop.y == end_b.y:
                stops_dict[idx] = stop
                self.end_b_key = idx
            else:
                stops_dict[idx] = stop
        self.routes_dict = stops_dict
        self.station = start_pt
        self.N = N

        #-------------------------------------------------#
        # Create List of Epoch Trials
        #-------------------------------------------------#
        route_list = []
        for run in range(epochs):
            route_a , route_b = self.route_maker()
            total_fitness = self.fitness(route_a) + self.fitness(route_b)
            if len(route_list) < N:
                route_list.append((total_fitness, route_a, route_b))
                route_list = sorted(route_list, key=lambda x: x[0])
            if total_fitness < route_list[-1][0]:
                route_list.pop()
                route_list.append((total_fitness, route_a, route_b))
                route_list = sorted(route_list, key=lambda x: x[0])
            else:
                continue
        self.route_list = route_list


    def route_maker(self):

        #-------------------------------------------------#
        # randomly assign stops to routes
        #-------------------------------------------------#
        exclude_stops = ['start', self.end_a_key, self.end_b_key]
        stop_ids = [stop for stop in self.routes_dict.keys() if stop not in exclude_stops]
        random.shuffle(stop_ids)
        route_a = ['start']
        route_b = ['start']
        while stop_ids:
            choose_route = np.random.choice(['a','b'])
            pop_pt = stop_ids.pop()
            if choose_route == 'a':
                route_a.append(pop_pt)
            else:
                route_b.append(pop_pt)
        #-------------------------------------------------#
        # append the end nodes
        #-------------------------------------------------#
        route_a.append(self.end_a_key)
        route_b.append(self.end_b_key)
        return route_a, route_b


    def fitness(self,route):
        travel_dist = 0
        current_node = None
        current_pt = None
        next_pt = None
        for node in route:
            if current_node == None:
                current_pt = node
                current_node = self.routes_dict[node]
                continue
            next_node = self.routes_dict[node]
            next_pt = node
            dist = next_node.distance(current_node)
            travel_dist += dist
            current_node = next_node
            current_pt = next_pt

        return travel_dist

    def score(self):
        size = self.bus_stops.shape[0]
        print('number of total stops = {}'.format(size))
        print()
        for num in range(self.N):
            score = self.route_list[num][0]
            a = self.route_list[num][1]
            b = self.route_list[num][2]
            print('Route Option {}: \nscore = {}'.format(num+1, score))
            print()


    def evolve(self, epochs):
        for i in range(epochs):
            for parent in self.route_list:
                indx = self.route_list.index(parent)
                parent_fitness = parent[0]
                parent_a = parent[1]
                parent_b = parent[2]

                # Make Random Slices
                rand_a = sorted(list(np.random.randint(1,high=len(parent_a)-1,size=2)))
                rand_b = sorted(list(np.random.randint(1,high=len(parent_b)-1,size=2)))

                # Slice the Routes
                a_start = [j for j in parent_a if parent_a.index(j) < rand_a[0]]
                a_end = [j for j in parent_a if parent_a.index(j) > rand_a[1]]

                b_start = [j for j in parent_b if parent_b.index(j) < rand_b[0]]
                b_end = [j for j in parent_b if parent_b.index(j) > rand_b[1]]

                #Shuffle the Bag
                a_bag = [j for j in parent_a if j not in a_start and j not in a_end]
                b_bag = [j for j in parent_b if j not in b_start and j not in b_end]
                mixed_bag = a_bag + b_bag
                random.shuffle(mixed_bag)

                # Assign Nodes to Routes
                while mixed_bag:
                    choose_route = np.random.choice(['a','b'])
                    pop_pt = mixed_bag.pop()
                    if choose_route == 'a':
                        a_start.append(pop_pt)
                    else:
                        b_start.append(pop_pt)

                child_a = a_start + a_end
                child_b = b_start + b_end

                # Evaluate Fitness of Child & Replace if Imporvement
                child_fitness = self.fitness(child_a) + self.fitness(child_b)
                if child_fitness < parent_fitness:
                    self.route_list.pop(indx)
                    self.route_list.insert(indx,(child_fitness, child_a, child_b))
                else:
                    continue

            #Sort the Winning Routes
            self.route_list = sorted(self.route_list)



    def plot(self):
        '''
        OUTPUT: plot of routes
        '''

        fig = plt.figure(figsize=(18,12))
        for n in range(self.N):
            # Make LineString Objects
            route_a_line = self.route_line(self.route_list[n][1])
            route_b_line = self.route_line(self.route_list[n][2])

            # Make Geo DataFrames
            route_a_geo = self.transform_to_GeoDataFrame(route_a_line)
            route_b_geo = self.transform_to_GeoDataFrame(route_b_line)

            ax = fig.add_subplot(2,2,n+1)

            ax.set_aspect('equal')
            self.roads.plot(ax=ax,color='black', linewidth=.5 )
            self.region.plot(ax=ax, color='orange', alpha=.2)
            self.bus_stops_geo.plot(ax=ax, color='red',markersize=8)

            route_a_geo.plot(ax=ax, color='green', linewidth=1)
            route_b_geo.plot(ax=ax, color='blue', linewidth=1)

            ax.set_title('East Side Route Map {}\nFitness = {}'.format(n+1,self.route_list[n][0]))
            ax.set_ylim((self.miny, self.maxy))
            ax.set_xlim((self.minx, self.maxx))
            ax.set_xticks([])
            ax.set_yticks([])

        plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.1, hspace=.1)
        plt.show()


    def route_line(self, route):
        '''
        INPUT: list of root id's
        OUTPUT: LineString object
        '''
        tuples = [(self.routes_dict[node].x, self.routes_dict[node].y) for node in route]
        return LineString(tuples)

    def transform_to_GeoDataFrame(self, geo_list):
        '''
        INPUT: list of geometry objects
        OUTPUT: GeoDataFrame
        '''
        geo_df = gpd.GeoDataFrame(GeoSeries(geo_list))
        geo_df.columns = ['geometry']
        geo_df.crs = {'init': 'epsg:4326'}
        geo_df.set_geometry('geometry',inplace=True)

        return geo_df
