from backcountry_mtn_us import __version__
from backcountry_mtn_us import backcountry_mtn_us as bm
import pandas as pd
import requests
import json
import numpy as np
from requests.exceptions import HTTPError
import pytest

def test_version():
    assert __version__ == '0.1.0'
    
def test_raise_exception():
    with pytest.raises(AssertionError or HTTPError):
        bm.get_data(triplet = '1159:WA:SNTL', days = '2')
        bm.get_closest_park(lat = 50, lng = -120, count = '3')
        bm.get_data_history(triplet = '1125:AZ:SNTL', startdate = '201-01-19', enddate = "2013-01-20")
        bm.get_state_park(state = AZ)
        
def test_get_state_stats():
    df = bm.get_state_stats()
    assert set(df.columns) == {'Max_Elevation', 'Avg_Elevation', 'State_Park_Count'}

    
def test_get_closest_park():
    df = bm.get_closest_park(lat = 50, lng = -120, count = 3)
    assert set(df.columns) == {'Distance (miles)', 
                               'Elevation (ft)', 
                               'Lat',
                               'Lng', 
                               'Name', 
                               'Timezone', 
                               'Triplet'}

def test_get_data():
    df = bm.get_data(triplet = '1159:WA:SNTL', days = 2)
    assert set(df.columns) == {'Date', 
                               'Snow Water Equivalent (in)', 
                               'Change In Snow Water Equivalent (in)',
                               'Snow Depth (in)', 
                               'Change In Snow Depth (in)', 
                               'Observed Air Temperature (degrees farenheit)'}


def test_get_state_park():
    df = bm.get_state_park(state = "AZ")
    assert set(df.columns) == {'Elevation', 
                               'Name', 
                               'Timezone',
                               'Triplet', 
                               'Lat', 
                               'Lng'}
    
def test_get_data_history():    
    df = bm.get_data_history(triplet = "1125:AZ:SNTL", startdate = "2013-01-19", enddate = "2013-01-20")   
    assert set(df.columns) == {'Date', 
                               'Snow Water Equivalent (in)', 
                               'Change In Snow Water Equivalent (in)',
                               'Snow Depth (in)', 
                               'Change In Snow Depth (in)', 
                               'Observed Air Temperature (degrees farenheit)'}
    
  
