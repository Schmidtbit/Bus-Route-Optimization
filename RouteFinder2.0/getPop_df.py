from myAPIs import census_API_key as key
import requests
import json
import pandas as pd


def makeAPI_PopByBlock2010(state, county,  key):
    '''
    INPUT:  (1) state FIPS code 
            (2) FIPS county code
            (3) API key to US Census
            
    OUTPUT: pandas DataFrame
    '''
    
    # Use API to get population data by census block
    base_url = 'https://api.census.gov/data/2010/sf1'
    query_call = '?get=P0010001'
    geo_call = '&for=block:*&in=state:{}&in=county:{}&'.format(state,county)
    key_call = 'key={}'.format(key)
    URL = base_url + query_call + geo_call + key_call
    response = requests.get(URL).json()
    data = response[1:]
    labels = response[0]
    
    # Create pandas DataFrame
    df = pd.DataFrame(data=data, columns=labels)
    # Rename population column
    df.rename(columns={'P0010001': 'population'}, inplace=True)
    # Create 'ID' column
    df['ID'] = df.state + df.county + df.tract + df.block
    
    return df



if __name__ == "__main__":
    key = key()
    state = str(input('enter state FIPS code (i.e. 48 for TX): '))
    county = str(input('enter county FIPS code (i.e. 453 for Travis): '))
