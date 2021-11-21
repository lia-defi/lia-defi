import requests
import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.indexes.base import Index
from pandas.io.html import read_html
import requests
from datetime import date, datetime
from requests.models import Response
from requests_html import HTMLSession, user_agent
import re
import json



def get_statements(symbol,name):
    
    url = f'https://www.macrotrends.net/stocks/charts/{symbol}/{name}/financial-statements'

    session=requests.Session()
    session.headers.update(
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
    
    response=session.get(url)

    #regex to find the data
    num=re.findall('(?<=div\>\"\,)[0-9\.\"\:\-\, ]*',response.text)
    text=re.findall('(?<=s\: \')\S+(?=\'\, freq)',response.text)

    #convert text to dict via json
    dicts=[json.loads('{'+i+'}') for i in num]

    #create dataframe
    df=pd.DataFrame()
    for ind,val in enumerate(text):
        df[val]=dicts[ind].values()
    df.index=dicts[ind].keys()

    return df

print(get_statements('AMZN','amazon'))
