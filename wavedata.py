import requests
import json
import pandas as pd
from valid import valid 

def wavedata(url1, url2, url3):
    url = valid(url1, url2, url3)

    if url == 'Error':
        return {"ChanceRain": 0, "Temperature": 0, "WaveDirection": 0, "WaveHeight": 0, "WavePeriod": 0, "WindDirection": 0, "WindSpeed": 0, "validTime": 0}
    else:
        r = requests.get(url)
        x = r.json()
        ## wave height
        wvht = x['properties']['waveHeight']['values']
        dwvht = pd.json_normalize(wvht)[:]
        #format the time string
        dwvht['validTime'] = dwvht['validTime'].str[0:16]
        #format value
        dwvht['value'] = round((dwvht['value']*3.28084).astype(float), 1)
        #convert to date/time
        dwvht['validTime'] = pd.to_datetime(dwvht['validTime'], format = '%Y-%m-%dT%H:%M')
        #rename
        dwvht = dwvht.rename(columns = {"value": "WaveHeight"})
        
        ##wave period
        wvpd = x['properties']['wavePeriod']['values']
        dwvpd = pd.json_normalize(wvpd)[:]
        #format the time string
        dwvpd['validTime'] = dwvpd['validTime'].str[0:16]
        #format value
        dwvpd['value'] = round(dwvpd['value'], 1)
        #convert to date/time
        dwvpd['validTime'] = pd.to_datetime(dwvpd['validTime'], format = '%Y-%m-%dT%H:%M')
        #rename
        dwvpd = dwvpd.rename(columns = {"value": "WavePeriod"})

        ##wave direction
        wvdir = x['properties']['waveDirection']['values']
        dwvdir = pd.json_normalize(wvdir)[:]
        #format the time string
        dwvdir['validTime'] = dwvdir['validTime'].str[0:16]
        #format value
        dwvdir['value'] = round(dwvdir['value'], 1)
        #convert to date/time
        dwvdir['validTime'] = pd.to_datetime(dwvdir['validTime'], format = '%Y-%m-%dT%H:%M')
        #rename
        dwvdir = dwvdir.rename(columns = {"value": "WaveDirection"})

        ##wind speed
        wnspd = x['properties']['windSpeed']['values']
        dwnspd = pd.json_normalize(wnspd)[:]
        #format the time string
        dwnspd['validTime'] = dwnspd['validTime'].str[0:16]
        #format value
        dwnspd['value'] = round((dwnspd['value']*0.621371).astype(float), 1)
        #convert to date/time
        dwnspd['validTime'] = pd.to_datetime(dwnspd['validTime'], format = '%Y-%m-%dT%H:%M')
        #rename
        dwnspd = dwnspd.rename(columns = {"value": "WindSpeed"})

        ##wind direction
        wndir = x['properties']['windDirection']['values']
        dwndir = pd.json_normalize(wndir)[:]
        #format the time string
        dwndir['validTime'] = dwndir['validTime'].str[0:16]
        #format value
        dwndir['value'] = round(dwndir['value'], 1)
        #convert to date/time
        dwndir['validTime'] = pd.to_datetime(dwndir['validTime'], format = '%Y-%m-%dT%H:%M')
        #rename
        dwndir = dwndir.rename(columns = {"value": "WindDirection"})

        ## temp
        temp = x['properties']['temperature']['values']
        dtemp = pd.json_normalize(temp)[:]
        #format the time string
        dtemp['validTime'] = dtemp['validTime'].str[0:16]
        #format value
        dtemp['value'] = round(((dtemp['value']*1.8)+32).astype(float), 1)
        #convert to date/time
        dtemp['validTime'] = pd.to_datetime(dtemp['validTime'], format = '%Y-%m-%dT%H:%M')
        #rename
        dtemp = dtemp.rename(columns = {"value": "Temperature"})

        ##chance of rain
        rainperc = x['properties']['probabilityOfPrecipitation']['values']
        drainperc = pd.json_normalize(rainperc)[:]
        #format the time string
        drainperc['validTime'] = drainperc['validTime'].str[0:16]
        #format value
        drainperc['value'] = round(drainperc['value'], 1)
        #convert to date/time
        drainperc['validTime'] = pd.to_datetime(drainperc['validTime'], format = '%Y-%m-%dT%H:%M')
        #rename
        drainperc = drainperc.rename(columns = {"value": "ChanceRain"})

        

        #create a dataframe for time slots
        forecast = pd.Series(pd.date_range(dwvht['validTime'][0], freq='H', periods=36), name="validTime")
        forecast = forecast.to_frame()
        forecast['validTime'] = pd.to_datetime(forecast['validTime'], format = '%Y-%m-%dT%H:%M')

        #join results
        stage = forecast.merge(dwvht, on='validTime', how='left')

        #second join
        stage2 = stage.merge(dwvpd, on='validTime', how='left')

        # third join
        stage3 = stage2.merge(dwvdir, on='validTime', how='left')

        # fourth join
        stage4 = stage3.merge(dwnspd, on='validTime', how='left')

        # fifth join
        stage5 = stage4.merge(dwndir, on='validTime', how='left')

        # sixth join
        stage6 = stage5.merge(dtemp, on='validTime', how='left')

        # seventh join
        stage7 = stage6.merge(drainperc, on='validTime', how='left')

        #interpolate
        results = stage7.interpolate(method ='linear', limit_direction = 'forward', axis = 0)

        rounded = results.round(decimals=1)

        result_json = rounded.to_json(orient = 'records', indent=4, date_format = 'iso')

        parsed = json.loads(result_json)

        return parsed