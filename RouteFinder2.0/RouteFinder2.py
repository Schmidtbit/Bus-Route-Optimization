

class RouteMaker2:
    def __init__(self, stops_df, AoA_df):
        self.stops_df = stops_df
        self.AoA_df = AoA_df
        self.LatLong = {'init', 'EPSG:4326'}

        # Populated with .define_system() method
        self.GPS = None
        self.nRoutes = None
        self.station = None


    def define_system(self, station, nRoutes):
        self.station = station
        self.nRoutes = nRoutes
        input_msg = input('Input NAD83 EPSG Code\n(Example: \'2277\' for Texas North Central, USA)\nEPSG:')
        self.GPS = {'init', 'EPSG:{}'.format(input_msg)}
