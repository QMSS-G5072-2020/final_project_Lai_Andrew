import pandas as pd
import requests
import json
import numpy as np
from requests.exceptions import HTTPError

def get_closest_park(lat, lng, count):
    """
    Returns a pandas DataFrame of closest parks by latitude and longitude.
    
    Parameters:
    ------------
    lat : Latitude as an integer (must be within the bounds of -90 and 90)
    lng : Longitude as an integer (must be within the bounds of -180 and 180)
    count: How many parks you want returned based on your lat,lng. An integer input.
    
    Output:
    ------------
    A pandas DataFrame object that describes distance, elevation, latitude, longitude, park name, 
    timezone, and triplet code (park id).
    
    Example:
    ------------
    >> get_closest_park(lat = 50, lng = -120, count = 3) 
    
    
    """
    
    assert isinstance(lat, int), "This function only works with arguments as integers."
    assert (-90 <= lat <= 90), "Latitude is out of bounds"
    assert (-180 <= lng <= 180), "Longitude is out of bounds"
    assert isinstance(lng, int), "This function only works with arguments as integers."
    assert isinstance(count, int), "This function only works with arguments with integers."
    assert (0 < count <= 5), "Count is out of bounds."
    
    try:
        params = {"lat":lat, "lng":lng, 'count':count}
        r = requests.get("http://api.powderlin.es/closest_stations",
                     params = params)
        r.raise_for_status()
        check = r.json()
        df = pd.json_normalize(check)
        df = df.drop(df.columns[[7]], axis=1)
        df.columns = ['Distance (miles)', 'Elevation (ft)', 'Lat', 'Lng', 'Name', 'Timezone', 'Triplet']
        df = df.round({'Distance (miles)': 2, 'Lat': 2 ,'Lng':2})
        return df
    
    except HTTPError as error:
        print(f'Something went wrong. Please check your connection again.{error}')
        
    

def get_data(triplet, days):
    
    """
    Returns a pandas DataFrame of detailing data of selected park .
    
    Parameters:
    ------------
    triplet : The park id code. In the format of IdNumber:StateAbbreviation:SNTL. A string.
    days : Number of days (not including today) you want to retrieve data for chosen park
    
    Output:
    ------------
    A pandas DataFrame object that describes date, snow water, change in snow water, snow depth, 
    change in snow depth, and temperature. 
    
    Example:
    ------------
    >> get_data(triplet = '1159:WA:SNTL', days = 2)
    
    
    """
    assert isinstance(triplet, str), "Stations only work as strings"
    assert isinstance(days, int) and days >= 0, "This function only works with days as integers and >= 0."
    
    try:
        url = 'http://api.powderlin.es/station/{}'.format(triplet)
        params = {'days':days}
        r = requests.get((url), 
                         params = params)
        r.raise_for_status()
        check = r.json()
        df = pd.json_normalize(check['data'])
        return df
    except HTTPError as error:
        print(f'This Mountain could not be found. Please check your triplet code again or lower amount of days. {error}')

        
def get_state_park(state):
    
    
    """
    Returns a pandas DataFrame of all parks by selected state.
    
    Parameters:
    ------------
    state : The state abbreviation/postal code. For example: California = CA. A string.
    
    Output:
    ------------
    A pandas DataFrame object that describes elevation, park name, timezone, triplet/park id, 
    latitude, and longitude. 
    
    Example:
    ------------
    >> get_state_park(state = "AZ")
    
    
    """
    assert isinstance(state, str), "State abbreviations only work as strings"
    
    try:
        state = ":"+state+":"
        r = requests.get("http://api.powderlin.es/stations")
        r.raise_for_status()
        check = r.json()
        df = pd.json_normalize(check)
        pd.set_option('display.max_rows', 150)
        df = df.drop(df.columns[[4]], axis=1)
        df.columns = ['Elevation', 'Name', 'Timezone', 'Triplet', 'Lat', 'Lng']
        df = df.round({'Lat': 2 ,'Lng':2})
        state_info = df[df['Triplet'].str.contains(state)]
        state_info.index = range(len(state_info.index))

        if state_info.empty:
            print("There is no data for this State.")
        else:
            return state_info
    
    except HTTPError as error: 
        print(f'Something went wrong. Please check your inputs again. {error}')

        
def get_state_stats():
    
    """
    Returns a pandas DataFrame that details summary statistics for each state recorded.
    
    Parameters:
    ------------
    None
    
    Output:
    ------------
    A pandas DataFrame object that describes max park elevation, average park elevation , and how many parks 
    are in each state. 
    
    Example:
    ------------
    >> get_state_stats()
    
    """
    
    try:
        r = requests.get("http://api.powderlin.es/stations")
        check = r.json()
        r.raise_for_status()
        df = pd.json_normalize(check)
        df['state'] = df['triplet'].str.extract('([A-Z]{2})',expand = True)
        stats = df.groupby("state").agg(
        Max_Elevation =('elevation', 'max'),
        Avg_Elevation = ('elevation', np.mean),
        State_Park_Count = ('state', 'count'))
        stats = stats.round({'Avg_Elevation': 2})
        return stats
    except HTTPError as error:
        print(f'Something went wrong. Please check your connection again. {error}')
        

def get_data_history(triplet, startdate, enddate):
    
    """
    Returns a pandas DataFrame of detailing historical data of selected park .
    
    Parameters:
    ------------
    triplet : The park id code. In the format of IdNumber:StateAbbreviation:SNTL. A string.
    startdate : Time period you want to start at. YYYY-MM-DD. A string. 
    enddate : Time period you want to end at. YYYY-MM-DD. A string. 
    
    Output:
    ------------
    A pandas DataFrame object that describes date, snow water, change in snow water, snow depth, 
    change in snow depth, and temperature. 
    
    Example:
    ------------
    >> get_data_history(triplet = "1125:AZ:SNTL", startdate = "2013-01-19", enddate = "2013-01-20")
    
    """
    
    
    try:
        assert isinstance(triplet, str), "Stations only work as strings"
        assert isinstance(startdate, str), "This function only works with arguments as strings."
        assert isinstance(enddate, str), "This function only works with arguments as strings."
        url = 'http://api.powderlin.es/station/{}'.format(triplet)
        params = {'start_date':startdate, 'end_date':enddate}
        r = requests.get((url), 
                         params = params)
        r.raise_for_status()
        check = r.json()
        df = pd.json_normalize(check['data'])
        return df
    except HTTPError as error:
        print(f'This Mountain could not be found. Please check your inputs again. {error}')
