import pytest
from railway import Station, RailNetwork
import re


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
    print("Actual error:",str(e.value))            
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
