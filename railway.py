import matplotlib.pyplot as plt
import numpy as np

def fare_price(distance, different_regions, hubs_in_dest_region): 
    """
    This function computes approximation of the cost of a rail fare between two stations.

    :param distance: Distance between two stations.
    :param different_regions: it is a Boolean value where it is 1 if the stations belong to different regions, and 0 otherwise.
    :param hubs_in_dest_region: Number of hub stations in the same region as the destination station.
    :return: The fare price
    """
    calculated_fare_price = 1 + (distance * np.exp(-distance/100) * (1 + (different_regions * hubs_in_dest_region)/10))
    return calculated_fare_price

class Station: #represents single station
    def __init__(self, name, region, crs, lat, lon, hub):
        # Check and store name as a string
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        self.name = name

        # Check and store region as a string
        if not isinstance(region, str):
            raise ValueError("Region must be a string")
        self.region = region

        # Check and store CRS code as a 3-character string consisting of uppercase letters
        if not isinstance(crs, str) or not crs.isalpha() or len(crs) != 3 or not crs.isupper():
            raise ValueError("CRS code must be a 3-character string of uppercase letters")
        self.crs = crs

        # Check and store latitude as a decimal number in the range [-90, 90]
        if not isinstance(lat, (float, int)) or lat < -90 or lat > 90:
            raise ValueError("Latitude must be a decimal number in the range [-90, 90]")
        self.lat = lat

        # Check and store longitude as a decimal number in the range [-180, 180]
        if not isinstance(lon, (float, int)) or lon < -180 or lon > 180:
            raise ValueError("Longitude must be a decimal number in the range [-180, 180]")
        self.lon = lon

        # Check and store hub as a boolean value
        if not isinstance(hub, bool):
            raise ValueError("Hub must be a boolean value")
        self.hub = hub

    def __str__(self):
        return f"Station({self.crs}-{self.name}/{self.region}{'-hub' if self.hub else ''})"
    
    def distance_to(self):
        raise NotImplementedError


class RailNetwork: #brings together all the stations from a dataset 
    def __init__(self, stations):
        self.stations = {}
        
        for station in stations:
            if station.crs in self.stations:
                raise ValueError(f"Duplicate CRS code: {station.crs} is not allowed in the same RailNetwork")
            
            self.stations[station.crs] = station

    def __str__(self):
        return f"RailNetwork(stations={list(self.stations.values())}"
    
    def regions(self):
        raise NotImplementedError

    def n_stations(self):
        raise NotImplementedError

    def hub_stations(self, region):
        raise NotImplementedError

    def closest_hub(self, s):
        raise NotImplementedError

    def journey_planner(self, start, dest):
        raise NotImplementedError

    def journey_fare(self, start, dest, summary):
        raise NotImplementedError

    def plot_fares_to(self, crs_code, save, ADDITIONAL_ARGUMENTS):
        raise NotImplementedError

    def plot_network(self, marker_size: int = 5) -> None:
        """
        A function to plot the rail network, for visualisation purposes.
        You can optionally pass a marker size (in pixels) for the plot to use.

        The method will produce a matplotlib figure showing the locations of the stations in the network, and
        attempt to use matplotlib.pyplot.show to display the figure.

        This function will not execute successfully until you have created the regions() function.
        You are NOT required to write tests nor documentation for this function.
        """
        fig, ax = plt.subplots(figsize=(5, 10))
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")
        ax.set_title("Railway Network")

        COLOURS = ["b", "r", "g", "c", "m", "y", "k"]
        MARKERS = [".", "o", "x", "*", "+"]

        for i, r in enumerate(self.regions):
            lats = [s.lat for s in self.stations.values() if s.region == r]
            lons = [s.lon for s in self.stations.values() if s.region == r]

            colour = COLOURS[i % len(COLOURS)]
            marker = MARKERS[i % len(MARKERS)]
            ax.scatter(lons, lats, s=marker_size, c=colour, marker=marker, label=r)

        ax.legend()
        plt.tight_layout()
        plt.show()
        return

    def plot_journey(self, start: str, dest: str) -> None:
        """
        Plot the journey between the start and end stations, on top of the rail network map.
        The start and dest inputs should the strings corresponding to the CRS codes of the
        starting and destination stations, respectively.

        The method will overlay the route that your journey_planner method has found on the
        locations of the stations in your network, and draw lines to indicate the route.

        This function will not successfully execute until you have written the journey_planner method.
        You are NOT required to write tests nor documentation for this function.
        """
        # Plot railway network in the background
        network_lats = [s.lat for s in self.stations.values()]
        network_lons = [s.lon for s in self.stations.values()]

        fig, ax = plt.subplots(figsize=(5, 10))
        ax.scatter(network_lons, network_lats, s=1, c="blue", marker="x")
        ax.set_xlabel("Longitude (degrees)")
        ax.set_ylabel("Latitude (degrees)")

        # Compute the journey
        journey = self.journey_planner(start, dest)
        plot_title = f"Journey from {journey[0].name} to {journey[-1].name}"
        ax.set_title(f"Journey from {journey[0].name} to {journey[-1].name}")

        # Draw over the network with the journey
        journey_lats = [s.lat for s in journey]
        journey_lons = [s.lon for s in journey]
        ax.plot(journey_lons, journey_lats, "ro-", markersize=2)

        plt.show()
        return


brighton = Station("Brighton", "South East", "BTN", 50.829659, -0.141234, True)
kings_cross = Station("London Kings Cross", "London", "KGX", 51.530827, -0.122907, True)
edinburgh_park = Station("Edinburgh Park", "Scotland", "EDP", 55.927615, -3.307829, False)

list_of_stations = [brighton, kings_cross, edinburgh_park]
rail_network = RailNetwork(list_of_stations)

print(f"List of stations passed in: {list_of_stations}")
print(f"Stations in the network: {list(rail_network.stations.values())}")
print(f"Keys of rail_network.stations: {list(rail_network.stations.keys())}")   #this operates as usual but it doesnt showcase the full string for some reason 06/11/2023

