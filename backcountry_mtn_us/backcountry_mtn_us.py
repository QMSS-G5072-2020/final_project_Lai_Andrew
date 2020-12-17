import requests
import json
import pandas as pd

def state_station(state):
    assert isinstance(state, str), "States only work as strings"
    state = ":"+state+":"
    r = requests.get("http://api.powderlin.es/stations")
    r.raise_for_status()
    check = r.json()
    df = pd.json_normalize(check)
    state_info = df[df['triplet'].str.contains(state)]
    if state_info.empty:
        print("There is no data for this State")
    else:
        return state_info
