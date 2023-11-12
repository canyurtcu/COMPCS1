import pytest
from railway import Station, RailNetwork, fare_price
import re
import numpy as np

def test_fare_price():
    distance = 1
    different_regions = 1
    hubs_in_dest_region = 1
    expected = 1 + (distance * np.exp(-distance/100) * (1 + (different_regions * hubs_in_dest_region)/10))
    assert expected == fare_price(distance,different_regions,hubs_in_dest_region)

def test_invalid_station_creation():  # Test creating a Station with invalid values
    with pytest.raises(ValueError) as e :   #Case: Name is not a string   
        Station(10, "South East", "BTN", 50.829659, -0.141234, True) 
    assert e.match("Name must be a string")

    with pytest.raises(ValueError) as e :   #Case: Region is not a string   
        Station('Brighton', 10, "BTN", 50.829659, -0.141234, True) 
    assert e.match("Region must be a string")

    with pytest.raises(ValueError) as e :   #Case: CRS code is not capital letters   
        Station('Brighton', 'South East', 'btn', 50.829659, -0.141234, True) 
    assert e.match("CRS code must be a 3-character string of uppercase letters")

    with pytest.raises(ValueError) as e :   #Case: CRS code is not 3 character long   
        Station('Brighton', 'South East', 'BTNN', 50.829659, -0.141234, True) 
    assert e.match("CRS code must be a 3-character string of uppercase letters")

    with pytest.raises(ValueError) as e :   #Case: CRS code is not a string   
        Station('Brighton', 'South East', 123, 50.829659, -0.141234, True) 
    assert e.match("CRS code must be a 3-character string of uppercase letters")

    with pytest.raises(ValueError) as e :   #Case: Latitude is greater than 90  
        Station('Brighton', "South East", "BTN", 100, -0.141234, True)           
    assert e.match(re.escape("Latitude must be a decimal number in the range [-90, 90]"))

    with pytest.raises(ValueError) as e :   #Case: Latitude is less than -90  
        Station('Brighton', "South East", "BTN", -100, -0.141234, True) 
    assert e.match(re.escape("Latitude must be a decimal number in the range [-90, 90]"))

    with pytest.raises(ValueError) as e :   #Case: Latitude is not an integer or float
        Station('Brighton', "South East", "BTN", '-100', -0.141234, True) 
    assert e.match(re.escape("Latitude must be a decimal number in the range [-90, 90]"))

    with pytest.raises(ValueError) as e :   #Case: Longitude is greater than 180  
        Station('Brighton', "South East", "BTN", 50.829659, 200, True) 
    assert e.match(re.escape("Longitude must be a decimal number in the range [-180, 180]"))   

    with pytest.raises(ValueError) as e :   #Case: Longitude is less than -180  
        Station('Brighton', "South East", "BTN", 50.829659, -200, True) 
    assert e.match(re.escape("Longitude must be a decimal number in the range [-180, 180]")) 
    
    with pytest.raises(ValueError) as e :   #Case: Longitude is not an integer or float
      Station('Brighton', "South East", "BTN", 50.829659, '200', True) 
    assert e.match(re.escape("Longitude must be a decimal number in the range [-180, 180]"))

    with pytest.raises(ValueError) as e:    #Case: Hub is not a boolean value
        Station('Brighton', "South East", "BTN", 50.829659, -0.141234, 'True')
    assert e.match("Hub must be a boolean value")

def test_distance_to():
    # Test the distance_to method
    station_a = Station("Station A", "Region A", "STA", 0, 0, True)
    station_b = Station("Station B", "Region B", "STB", 0, 1, True)
    R = 6371
    lat1, lon1, lat2, lon2 = np.radians([station_a.lat, station_a.lon, station_b.lat, station_b.lon])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    expected_distance = R * c

    assert station_a.distance_to(station_b) == expected_distance

def test_str_representation():
    # Test the __str__ method
    hub_station = Station("Hub Station", "Hub Region", "HUB", 0, 0, True)
    non_hub_station = Station("Non-Hub Station", "Non-Hub Region", "NHB", 0, 0, False)
    
    assert str(hub_station) == "Station(HUB-Hub Station/Hub Region-hub)"
    assert str(non_hub_station) == "Station(NHB-Non-Hub Station/Non-Hub Region)"

#Add __repr__ when you have figured it out

def test_railnetworkcreation():
    station_a = Station("Station A", "Region A", "STA", 0, 0, True)
    station_b = Station("Station B", "Region B", "STB", 0, 1, True)
    list_of_stations = [station_a,station_b]
    rail_network = RailNetwork(list_of_stations)
    expected_rail_network = [station_a, station_b]
    assert str(rail_network) == str(expected_rail_network)   #tests rail network creation

def test_CRS_duplicate_railnetwork():
    station_a = Station("Station A", "Region A", "STA", 0, 0, True) #tests for CRS duplicate in rail network creation
    station_a_duplicate = Station("Station A", "Region A", "STA", 0, 1, True)
    list_of_stations = [station_a,station_a_duplicate]

    with pytest.raises(ValueError) as e:
        RailNetwork(list_of_stations)
    assert e.match(f"Duplicate CRS code: STA is not allowed in the same RailNetwork")

def test_rail_network_regions():
    station_a = Station("Station A", "Region A", "STA", 0, 0, True)
    station_b = Station("Station B", "Region B", "STB", 0, 1, True)
    list_of_stations = [station_a,station_b]
    rail_network = RailNetwork(list_of_stations)
    expected_region = ["Region B", "Region A"]
    assert rail_network.regions() == expected_region    #tests region method

def test_rail_network_n_stations():
    station_a = Station("Station A", "Region A", "STA", 0, 0, True)
    station_b = Station("Station B", "Region B", "STB", 0, 1, True)
    list_of_stations = [station_a,station_b]
    rail_network = RailNetwork(list_of_stations)
    assert rail_network.n_stations() == 2   #tests n_stations method

def test_hub_stations():
    # Test the hub_stations method
    hub_station_a = Station("Hub Station A", "Region A", "HBA", 0, 0, True)
    hub_station_b = Station("Hub Station B", "Region B", "HBB", 0, 1, True)
    non_hub_station = Station("Non-Hub Station", "Region B", "NHB", 0, 2, False)
    
    rail_network = RailNetwork([hub_station_a, hub_station_b, non_hub_station])
    # Test without specifying a region
    assert len(rail_network.hub_stations()) == 2

    # Test specifying a region
    assert len(rail_network.hub_stations("Region B")) == 1

def test_hub_stations_regionexists():
    hub_station_a = Station("Hub Station A", "Region A", "HBA", 0, 0, True)
    hub_station_b = Station("Hub Station B", "Region B", "HBB", 0, 1, True)

    rail_network = RailNetwork([hub_station_a, hub_station_b])

    with pytest.raises(ValueError) as e:
        rail_network.hub_stations("C")
    print(str(e.value))
    assert e.match("Region 'C' does not exist in the network.")

# def test_closest_hub():
#     # Test the closest_hub method
#     hub_station_a = Station("Hub Station A", "Region A", "HBA", 0, 0, True)
#     non_hub_station_a = Station("Non-Hub Station A", "Region A", "NHA", 0, 1, False)
#     hub_station_b = Station("Hub Station B", "Region B", "HBB", 0, 2, True)
#     non_hub_station_b = Station("Non-Hub Station B", "Region B", "NHB", 0, 3, False)

#     rail_network = RailNetwork([hub_station_a, non_hub_station_a, hub_station_b, non_hub_station_b])

#     # Test when a hub station exists in the same region
#     assert rail_network.closest_hub(non_hub_station_a) == hub_station_a

#     # Test when a hub station exists in a different region
#     assert rail_network.closest_hub(non_hub_station_b) == hub_station_b