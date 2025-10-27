# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 13:39:55 2025

@author: roy
"""
import requests,pandas as pd
from fastmcp import FastMCP

mcp = FastMCP("air_quality")

api_url = 'https://data.moenv.gov.tw/api/v2/aqf_p_01'
token = '' # input your token or use env to set your access token
headers = {'accept': 'application/json'}

location = ['澎湖', '金門', '馬祖', '花東', '宜蘭', '高屏', '雲嘉南', '中部', '竹苗', '北部']
aqi_condition = {'良好':'aqi介於0到50','普通':'aqi介於51到100','對敏感族群不健康':'aqi介於101到150',
                 '對所有族群不健康':'aqi介於151到200','非常不健康':'aqi介於201到300','危害':'aqi介於301到500',}


@mcp.tool()
def location_name():
    """
    取得可查詢的地點或區域
    
    Args:

    Returns:
        str: 可查詢台灣未來三天空氣品質(包含今天)區域

    """
    return '可選擇縣市'+' : '+', '.join(location)

@mcp.tool()
def aqi_define():
    """
    空氣品質指標(AQI)燈號意義
    
    Args:

    Returns:
        str: 台灣AQI燈號定義

    """
    return '空氣品質指標(AQI)定義: '+', '.join(aqi_condition)

@mcp.tool()
def data_get():
    """
    台灣未來三天空氣品質情況與數據
    
    Args:

    Returns:
        dict: 台灣未來三天空氣品質數據

    """
    params = {'language':'zh','api_key':token,'offset':0}
    response = requests.get(api_url, headers=headers, params=params)
    t = response.json()
    nf = t['records']
    df = pd.DataFrame(nf).iloc[0:40,:]
    content = df['content'].iloc[0]
    publishtime = df['publishtime'].iloc[0]
    data = df[['forecastdate','area','majorpollutant','aqi']].to_dict(orient='records')
    need = {'content':content,'publishtime':publishtime,'record':data}
    return need

mcp.run(host='0.0.0.0',port=2080,transport='sse') # choose your port or host
