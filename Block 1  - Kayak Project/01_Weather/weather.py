import asyncio 
import requests
import pandas as pd
import json
from urllib.parse import urlencode, urlunparse
from pathlib import Path

def get_weather_data():
    #Open the file used as basis for the analysis. IT should have the insee code and the name of each citys
    path = Path('C:/Users/Utilisateur/Documents/JEDHA/03_Data_Collection_and_Management/04_Kayak_Project/00_Cities/coordinates.csv')
    df = pd.read_csv(path)

    #Create an empty dataframe with the needed columns
    df_weather = pd.DataFrame(columns=['city','code_insee','datetime','rr10','rr1','tmin','tmax','wind10m','gust10m'])

    #Request the database for each insee code
    for code_insee in df['code_insee'].unique():
        url = 'https://api.meteo-concept.com/api/forecast/daily?'
        params = {
            'token': "e3d5025f48dd7dd7109ef9323194feaad5f9f639e58cd8d77df7e700e49f0777",
            'insee': code_insee,
            
        }
        r = requests.get(url=url,params=params)

        if r.status_code == 400: 
            print(r.json()['message'])
            return df_weather
            
        else:
            list_forecast = r.json()['forecast']
            #Inside the json, there is a list of forecast for the next 14 days. We loop on the 7 next days and stoire the data and add it in the dataframe
            for forecast in list_forecast[1:8]:
                new_row = pd.DataFrame(
                    {
                        'city' : [df[df['code_insee'] == code_insee]['city'].iloc[0]],
                        'code_insee' : [code_insee],
                        'datetime':[ forecast['datetime']] ,
                        'rr10' : [forecast['rr10']] ,
                        'rr1': [forecast['rr1']],
                        'probarain': [forecast['probarain']],
                        'tmin': [forecast['tmin']],
                        'tmax' : [forecast['tmax']],
                        'wind10m' : [forecast['wind10m']],
                        'gust10m' : [forecast['gust10m']]
                    }
                )
                df_weather = df_weather.dropna(axis=1, how='all')
                df_weather = pd.concat([df_weather,new_row],ignore_index=True)

    #Get the final dataframe
    return df_weather

def get_city_ranking(df_weather,tmin=20,tmax=35,rainmax=10,windmax=50):

    #Add a coloum to know if a day is rainy/cold/hot/windy. The ranking will be done based on the number of days that have a low number of days not in the scipe
    df_weather['rainy_day'] = 0
    df_weather['cold_day'] = 0
    df_weather['hot_day'] = 0
    df_weather['windy_day'] = 0
    df_weather['total_day'] = 0

    #Switch the one for each day that are not in the scope
    df_weather.loc[df_weather['tmax'] >= tmax, 'hot_day'] = 1
    df_weather.loc[df_weather['tmax'] <tmin, 'cold_day'] = 1
    df_weather.loc[df_weather['rr1'] >rainmax, 'rainy_day'] = 1
    df_weather.loc[df_weather['rr10'] >rainmax, 'rainy_day'] = 1
    df_weather.loc[df_weather['wind10m'] >windmax, 'windy_day'] = 1
    df_weather.loc[df_weather['gust10m'] >windmax, 'windy_day'] = 1

    #For each day, if any of the columns is 1, we put the total by 1
    df_weather['total_day'] =  df_weather[['hot_day', 'cold_day', 'rainy_day','windy_day']].max(axis=1)

    #Pivot the table to get the info by cities. It is then sorted by the number of days in the scope and by the average rain 
    df_aggregated = df_weather.groupby('city')[['total_day','rainy_day','cold_day','hot_day','windy_day','rr10', 'rr1', 'tmin', 'tmax','wind10m','gust10m']].agg(['sum', 'mean']).reset_index()
    df_aggregated.columns = ['_'.join(col).strip() if col[1] else col[0] for col in df_aggregated.columns.values]
    df_aggregated=  df_aggregated.sort_values(by=['total_day_sum','rr10_mean'],ignore_index=True)

    #remove the extra columns
    columns_to_remove = ['total_day_mean','rainy_day_mean','cold_day_mean','hot_day_mean','windy_day_mean','tmin_sum','tmax_sum','wind10m_sum','gust10m_sum','rr10_sum','rr1_sum']
    for column in columns_to_remove:
        del df_aggregated[column] 

    #Add an index
    df_aggregated['id'] = df_aggregated.index + 1

    return df_aggregated

def save_weather_data(df_weather, df_aggregated):
    df_weather.to_csv('C:/Users/Utilisateur/Documents/JEDHA/03_Data_Collection_and_Management/04_Kayak_Project/00_Cities/weather.csv',header=True ,index=False)
    df_aggregated.to_csv('C:/Users/Utilisateur/Documents/JEDHA/03_Data_Collection_and_Management/04_Kayak_Project/00_Cities/weather_aggregated.csv',header=True ,index=False)

def read_weather_data():
    path = Path('C:/Users/Utilisateur/Documents/JEDHA/03_Data_Collection_and_Management/04_Kayak_Project/00_Cities/weather.csv')
    df_weather = pd.read_csv(path)
    
    path = Path('C:/Users/Utilisateur/Documents/JEDHA/03_Data_Collection_and_Management/04_Kayak_Project/00_Cities/weather_aggregated.csv')
    df_aggregated = pd.read_csv(path)

    return(
        df_weather,
        df_aggregated
    )