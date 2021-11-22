from numpy import RankWarning
import pandas as pd
from bs4 import BeautifulSoup
from pandas.core.indexes.base import Index
from pandas.io.html import read_html
import requests
from datetime import date, datetime
from requests.api import head
from requests.models import Response
from requests.sessions import session
from requests_html import HTMLSession, user_agent
import json
import time
import re


#response = requests.request("GET", url)
#source lia/bin/activate

class Scraper():
    def scrapedata(self):
        url = "https://investor.ryanair.com/wp-content/uploads/ryr-business-numbers/data.json"
        s = HTMLSession()
        r = s.get(url)
        data = r.json()
        return data

    def weather(self,query):
        url = f'https://www.google.com/search?q=weather+{query}'
        s = HTMLSession()
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        r = s.get(url,headers = headers)
        dict_weather = {
                "temp": r.html.find('span#wob_tm',first=True).text,
                "unit": r.html.find('div.vk_bk.wob-unit',first=True).find('span.wob_t',first=True).text,
                "desc": r.html.find('div.VQF4g',first=True).find('span#wob_dc',first=True).text
        }
        return dict_weather

    def edgar_insider(self,cik):
        s = HTMLSession()
        user_agent = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
        url = f'https://data.sec.gov/api/xbrl/companyconcept/{cik}/us-gaap/AccountsPayableCurrent.json'
        r = s.get(url,headers=user_agent)
        return r.content

    def insider_information(self,cik):
        s = HTMLSession()
        url = f'https://www.sec.gov/cgi-bin/own-disp?action=getissuer&CIK={cik}'
        r = pd.read_html(url)
        r = r[6]
        result = r.to_json(orient='columns')
        return result

    def Institutional_Holding(self):
        r = pd.read_csv('Institutional Holding.csv)
        result = r.to_dict()
            return result

    def get_cik_from_symbol(self,symbol):
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        table = pd.read_html(url)
        table = table[0]
        tickers = table['Symbol'].values.tolist()
        cik = table['CIK'].values.tolist()
        result = pd.DataFrame({'tickers':tickers,'cik':cik},index=tickers)
        result =  result.loc[symbol]
        result = result.to_dict()
        return result
    def url(self,symbol,name):
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
        s = HTMLSession()
        url = f'https://www.macrotrends.net/stocks/charts/{symbol}/{name}/financial-statements'
        return url

    def scrape(self,url,**kwargs):
        
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})
        
        response=session.get(url,**kwargs)

        return response


    def etl(self,response):

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
        
        return df.to_dict()
    
    def get_statements(self,sym,name,freq):
    
        url = f'https://www.macrotrends.net/stocks/charts/{sym}/{name}/financial-statements?freq={freq}'

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

    def financial_ratios(self,sym,name,freq):
        url = f'https://www.macrotrends.net/stocks/charts/{sym}/{name}/financial-ratios?freq={freq}'

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
    
    def cash_flow(self,sym,name,freq):
        url = f'https://www.macrotrends.net/stocks/charts/{sym}/{name}/cash-flow-statement?freq={freq}'

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

    def balance_sheet(self,sym,name,freq):
        url = f'https://www.macrotrends.net/stocks/charts/{sym}/{name}/balance-sheet?freq={freq}'

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

    def gdp_by_country(self):
        url = f'https://www.macrotrends.net/countries/ranking/gdp-gross-domestic-product'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = (df.to_dict())
        return df   

    def gdp_growth_rate(self):
        url = f'https://www.macrotrends.net/countries/ranking/gdp-growth-rate'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = (df.to_dict())
        return df   

    def gdp_per_capita(self):
        url = f'https://www.macrotrends.net/countries/ranking/gdp-per-capita'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = (df.to_dict())
        return df   

    def gross_national_income(self):
        url = f'https://www.macrotrends.net/countries/ranking/gni-gross-national-income'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = (df.to_dict())
        return df   

    def gross_national_income_by_country(self):
        url = f'https://www.macrotrends.net/countries/ranking/gni-per-capita'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df   

    def debt_to_gdp(self):
        url = f'https://www.macrotrends.net/countries/ranking/debt-to-gdp-ratio'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df   

    def gnp_by_country(self):
        url = f'https://www.macrotrends.net/countries/ranking/gnp-gross-national-product'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df   

    def inflation_rate(self):
        url = f'https://www.macrotrends.net/countries/ranking/inflation-rate-cpi'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 

    def manufacturing_output(self):
        url = f'https://www.macrotrends.net/countries/ranking/manufacturing-output'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 

    def trade_balance_deficit(self):
        url = f'https://www.macrotrends.net/countries/ranking/trade-balance-deficit'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 
    
    def trade_to_gdp(self):
        url = f'https://www.macrotrends.net/countries/ranking/trade-gdp-ratio'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 

    def exports_by_country(self):
        url = f'https://www.macrotrends.net/countries/ranking/exports'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 
    
    def imports_by_country(self):
        url = f'https://www.macrotrends.net/countries/ranking/imports'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 
    
    def foreign_direct_investment_by_country(self):
        url = f'https://www.macrotrends.net/countries/ranking/foreign-direct-investment'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 

    def tariff_rates(self):
        url = f'https://www.macrotrends.net/countries/ranking/tariff-rates'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 

    def tourism_statistics(self):
        url = f'https://www.macrotrends.net/countries/ranking/tourism-statistics'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 

    def healthcare_spending(self):
        url = f'https://www.macrotrends.net/countries/ranking/healthcare-spending'
        session=requests.Session()
        session.headers.update(
                {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
        response=session.get(url)

            #regex to find the data
        soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
        table = soup.find('table')
        row_data = []
        for row in table.find_all('tr'):
            col = row.find_all('td')
            col = [el.text.strip() for el in col]
            row_data.append(col)
        df = pd.DataFrame(row_data)
        df = df.to_dict()
        return df 












s = HTMLSession()
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}


def crude_oil_production_usa():
    url = f'https://www.eia.gov/dnav/pet/pet_crd_crpdn_adc_mbbl_m.htm'

    session=requests.Session()
    session.headers.update(
            {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'})    
    response=session.get(url)

            #regex to find the data
    soup = BeautifulSoup(response.text,'lxml')

            #convert text to dict via json
    table = soup.find_all('table')
    row_data = []
    for row in table.find_all('tr'):
        col = row.find_all('td')
        col = [el.text.strip() for el in col]
        row_data.append(col)
    df = pd.DataFrame(row_data)
    #df = df.to_dict()
    return df 


#button = class='x0o17e-0 DChGS'


'''''
selectedcompany = 'TYSON FOODS, INC.'
selectedreport = '10-Q'
csv = pd.read_csv('edgarfills.txt',sep='\t',lineterminator='\n',names=None)
csv.columns.values[0] = 'Item'
companyreport = csv[(csv['Item'].str.contains(selectedcompany))&(csv['Item'].str.contains(selectedreport))]
Filing = companyreport['Item'].str.split('|')
Filing = Filing.to_list()

for item in Filing[0]:
    if 'txt' in item:
        report = item
        report = report.replace(".txt","-index.html")
report = str.strip(report)
url = 'https://www.sec.gov/Archives/' + report
url = s.get(url, headers=headers)

df = pd.read_html(url.content)
document_index = df[0]
document_index = document_index.dropna()
document_name = document_index[document_index['Description'].str.contains(selectedreport)]
document_name = document_name['Document'].str.split(' ')
document_name = document_name[0][0]
report_formatted = report.replace('-','').replace('index.html','')
url = 'https://www.sec.gov/Archives/' + report_formatted + '/' + document_name
url = s.get(url,headers=headers)
df = pd.read_html(url.content)


df1 = dict((key, val) for k in df for key, val in k.items())
df2 = dict(df[0])
df3 = pd.DataFrame.from_records(df)


for item in df1:
    BS = (item.str.contains('Inventories') | item.str.contains('Total Assets'))
    if BS.any():
        Balance_Sheet = item
        print(Balance_Sheet)
'''
