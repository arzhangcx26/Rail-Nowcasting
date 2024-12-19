import pandas as pd
import requests
from datetime import datetime
#from dateutil.relativedelta import relativedelta

frequency_hierarchy = {
    'A' : 1,
    'SA' : 2,
    'Q' : 3,
    'M' : 4,
    'W' : 5,
    'D' : 6
}

# Create function that outputs API parameters to easily request different queries
def api_params(search_text: str, api_key: str):
    # Set the parameters for the data series that you want to retrieve
    return {
        'file_type': 'json',
        'search_text': search_text,
        'search_type': 'full_text',
        'order_by': 'search_rank',
        'limit': 20,
        'api_key': api_key
    }

def freq_checker(search_list, frequency: str):
    global frequency_hierarchy
    frequency = frequency.upper()

    search_list_new = []
    for result in search_list:
        result_freq = result['frequency_short']
        if frequency_hierarchy[result_freq] >= frequency_hierarchy[frequency]:
            search_list_new.append(result)

    return search_list_new

def search_database(search_text: str, api_key: str):
    # Set the base URL for the FRED API
    base_url = 'https://api.stlouisfed.org/fred/series/search?'
    
    # Send the request to the FRED API to retrieve the data series
    response = requests.get(base_url, params=api_params(search_text, api_key), verify = False)
    
    search_list = response.json()['seriess']
    
    return(search_list)

def find_best_series(search_list, frequency):
    global frequency_hierarchy
    frequency = frequency.upper()
    for result in search_list:
        result_freq = result['frequency_short']
        if frequency_hierarchy[result_freq] >= frequency_hierarchy[frequency]:
            return result['id']
    return None