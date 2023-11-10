from pathlib import Path
import csv
from typing import List
from railway import RailNetwork, Station

def read_rail_network(file_path: Path) -> RailNetwork:
    stations: List[Station] = []

    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Extract values from the row based on header information
            name = row.get('name', '')
            region = row.get('region', '')
            crs = row.get('crs', '')
            lat = float(row.get('latitude', 0.0))
            lon = float(row.get('longitude', 0.0))
            hub = bool(int(row.get('hub', 0)))
            stations.append(Station(name, region, crs, lat, lon, hub))
    return RailNetwork(stations)


    # file = open(filepath)
    # csvreader = csv.reader(file)
    # header = []
    # header = next(csvreader)
    # rows = []
    # for row in csvreader:
    #     rows.append(row)
    # print(rows)
    # file.close()
