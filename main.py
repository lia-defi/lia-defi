from fastapi import FastAPI, Path, Query, HTTPException
from pandas._config.config import describe_option
from pandas.io import html
from scraper import Scraper
from typing import Optional

app = FastAPI()
quotes = Scraper()

#copy and paste in terminal
#uvicorn main:app --reload

@app.get("/lia-defi")
def welcome():
    return {"Welcome to Lia"} 

@app.get("/lia-defi/ryanairdata")
async def read_item():
    return quotes.scrapedata()


@app.get("/lia-defi/weather/{cat}")
async def read_cat(cat: str = Path(None,description="Insert the name of the city")):
    return quotes.weather(cat)
    raise HTTPException(status_code=404, detail="City not found")

@app.get("/lia-defi/insidertrading/{cat}")
async def read_cat(cat: str = Path(None,description='Insert the CIK of the company')):
    return quotes.insider_information(cat)
    raise HTTPException(status_code=404, description="Control the CIK")

@app.get("/lia-defi/istitutionalholding")
async def read_cat():
    return quotes.Institutional_Holding()
    raise HTTPException(status_code=404, description="Rate limit exceeded")

@app.get("/lia-defi/getcikfromsp500/{cat}")
async def read_cat(cat: str = Path(None,description='Insert the CIK of the company')):
    return quotes.get_cik_from_symbol(cat)
    raise HTTPException(status_code=404, description="Control the Symbol")

@app.get("/lia-defi/getfinancialsummary/{cat}/{cats}/{subcat}")
async def read_cat(cat: str = Path(None,description='Insert the symbol with higher case letters of the company'),
cats: str = Path(None,description='insert the name of the company in lower letter'),
subcat: str =  Path(None,description='Q for quaterly and A for annually')):
    return quotes.get_statements(cat,cats,subcat)
    raise  HTTPException(status_code=404, description="Control the Symbol and the name of the company")

@app.get("/lia-defi/getfinancialratio/{cat}/{cats}/{subcat}")
async def read_cat(cat: str = Path(None,description='Insert the symbol with higher case letters of the company'),
cats: str = Path(None,description='insert the name of the company in lower letter'),
 subcat: str =  Path(None,description='Q for quaterly and A for annually')):
    return quotes.financial_ratios(cat,cats,subcat)
    raise  HTTPException(status_code=404, description="Control the Symbol and the name of the company")

@app.get("/lia-defi/getcashflow/{cat}/{cats}/{subcat}")
async def read_cat(cat: str = Path(None,description='Insert the symbol with higher case letters of the company'),
cats: str = Path(None,description='insert the name of the company in lower letter'),
 subcat: str = Path(None,description='Q for quaterly and A for annually')):
    return quotes.cash_flow(cat,cats,subcat)
    raise  HTTPException(status_code=404, description="Control the Symbol and the name of the company")

@app.get("/lia-defi/getcashflow/{cat}/{cats}/{subcat}")
async def read_cat(cat: str = Path(None,description='Insert the symbol with higher case letters of the company'),
cats: str = Path(None,description='insert the name of the company in lower letter'),
 subcat: str = Path(None,description='Q for quaterly and A for annually')):
    return quotes.balance_sheet(cat,cats,subcat)
    raise  HTTPException(status_code=404, description="Control the Symbol and the name of the company")

@app.get("/lia-defi/getgdp")
async def getgdp(q: Optional[str]=Query(None,description='GDP ranking by country')):
    return quotes.gdp_by_country()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/getgrowthrate")
async def getgrowthrate(q: Optional[str]=Query(None,description='Annual percentage growth rate of GDP at market prices based on constant local currency. Aggregates are based on constant 2010 U.S. dollars. GDP is the sum of gross value added by all resident producers in the economy plus any product taxes and minus any subsidies not included in the value of the products. It is calculated without making deductions for depreciation of fabricated assets or for depletion and degradation of natural resources.')):
    return quotes.gdp_growth_rate()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/getgdppercapita")
async def getgdppercapita(q: Optional[str]=Query(None,description='GDP per capita is gross domestic product divided by midyear population. GDP is the sum of gross value added by all resident producers in the economy plus any product taxes and minus any subsidies not included in the value of the products. It is calculated without making deductions for depreciation of fabricated assets or for depletion and degradation of natural resources. Data are in current U.S. dollars.')):
    return quotes.gdp_per_capita()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/getgrossnationalincome")
async def getgrossnationalincome(q: Optional[str]=Query(None,description='GNI (formerly GNP) is the sum of value added by all resident producers plus any product taxes (less subsidies) not included in the valuation of output plus net receipts of primary income (compensation of employees and property income) from abroad. Data are in current U.S. dollars. GNI, calculated in national currency, is usually converted to U.S. dollars at official exchange rates for comparisons across economies, although an alternative rate is used when the official exchange rate is judged to diverge by an exceptionally large margin from the rate actually applied in international transactions. To smooth fluctuations in prices and exchange rates, a special Atlas method of conversion is used by the World Bank. This applies a conversion factor that averages the exchange rate for a given year and the two preceding years, adjusted for differences in rates of inflation between the country, and through 2000, the G-5 countries (France, Germany, Japan, the United Kingdom, and the United States). From 2001, these countries include the Euro area, Japan, the United Kingdom, and the United States.')):
    return quotes.gross_national_income()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/getgrossnationalincomepercapita")
async def getgrossnationalincomepercapita(q: Optional[str]=Query(None,description='GNI per capita (formerly GNP per capita) is the gross national income, converted to U.S. dollars using the World Bank Atlas method, divided by the midyear population. GNI is the sum of value added by all resident producers plus any product taxes (less subsidies) not included in the valuation of output plus net receipts of primary income (compensation of employees and property income) from abroad. GNI, calculated in national currency, is usually converted to U.S. dollars at official exchange rates for comparisons across economies, although an alternative rate is used when the official exchange rate is judged to diverge by an exceptionally large margin from the rate actually applied in international transactions. To smooth fluctuations in prices and exchange rates, a special Atlas method of conversion is used by the World Bank. This applies a conversion factor that averages the exchange rate for a given year and the two preceding years, adjusted for differences in rates of inflation between the country, and through 2000, the G-5 countries (France, Germany, Japan, the United Kingdom, and the United States). From 2001, these countries include the Euro area, Japan, the United Kingdom, and the United States.')):
    return quotes.gross_national_income_by_country()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/debtogdp")
async def read(q: Optional[str]=Query(None,description='Debt is the entire stock of direct government fixed-term contractual obligations to others outstanding on a particular date. It includes domestic and foreign liabilities such as currency and money deposits, securities other than shares, and loans. It is the gross amount of government liabilities reduced by the amount of equity and financial derivatives held by the government. Because debt is a stock rather than a flow, it is measured as of a given date, usually the last day of the fiscal year.')):
    return quotes.debt_to_gdp()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/gnpbycountry")
async def read(q: Optional[str]=Query(None,description='GNI (formerly GNP) is the sum of value added by all resident producers plus any product taxes (less subsidies) not included in the valuation of output plus net receipts of primary income (compensation of employees and property income) from abroad. Data are in current U.S. dollars. GNI, calculated in national currency, is usually converted to U.S. dollars at official exchange rates for comparisons across economies, although an alternative rate is used when the official exchange rate is judged to diverge by an exceptionally large margin from the rate actually applied in international transactions. To smooth fluctuations in prices and exchange rates, a special Atlas method of conversion is used by the World Bank. This applies a conversion factor that averages the exchange rate for a given year and the two preceding years, adjusted for differences in rates of inflation between the country, and through 2000, the G-5 countries (France, Germany, Japan, the United Kingdom, and the United States). From 2001, these countries include the Euro area, Japan, the United Kingdom, and the United States.')):
    return quotes.gnp_by_country()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/inflationrate")
async def read(q: Optional[str]=Query(None,description='Inflation as measured by the consumer price index reflects the annual percentage change in the cost to the average consumer of acquiring a basket of goods and services that may be fixed or changed at specified intervals, such as yearly. The Laspeyres formula is generally used.')):
    return quotes.inflation_rate()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')


@app.get("/lia-defi/manufacturingoutput")
async def read(q: Optional[str]=Query(None,description='Manufacturing refers to industries belonging to ISIC divisions 15-37. Value added is the net output of a sector after adding up all outputs and subtracting intermediate inputs. It is calculated without making deductions for depreciation of fabricated assets or depletion and degradation of natural resources. The origin of value added is determined by the International Standard Industrial Classification (ISIC), revision 3. Data are in current U.S. dollars.')):
    return quotes.manufacturing_output()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/trade_balance_deficit")
async def read(q: Optional[str]=Query(None,description='External balance on goods and services (formerly resource balance) equals exports of goods and services minus imports of goods and services (previously nonfactor services). Data are in current U.S. dollars.')):
    return quotes.trade_balance_deficit()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')


@app.get("/lia-defi/trade_gdp_ratio")
async def read(q: Optional[str]=Query(None,description='Trade is the sum of exports and imports of goods and services measured as a share of gross domestic product.')):
    return quotes.trade_to_gdp()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/exports")
async def read(q: Optional[str]=Query(None,description='Exports of goods and services represent the value of all goods and other market services provided to the rest of the world. They include the value of merchandise, freight, insurance, transport, travel, royalties, license fees, and other services, such as communication, construction, financial, information, business, personal, and government services. They exclude compensation of employees and investment income (formerly called factor services) and transfer payments. Data are in current U.S. dollars.')):
    return quotes.exports_by_country()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/foreign_direct_investment")
async def read(q: Optional[str]=Query(None,description='Foreign direct investment refers to direct investment equity flows in the reporting economy. It is the sum of equity capital, reinvestment of earnings, and other capital. Direct investment is a category of cross-border investment associated with a resident in one economy having control or a significant degree of influence on the management of an enterprise that is resident in another economy. Ownership of 10 percent or more of the ordinary shares of voting stock is the criterion for determining the existence of a direct investment relationship. Data are in current U.S. dollars.')):
    return quotes.foreign_direct_investment_by_country()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/tariff_rates")
async def read(q: Optional[str]=Query(None,description='Weighted mean applied tariff is the average of effectively applied rates weighted by the product import shares corresponding to each partner country. Data are classified using the Harmonized System of trade at the six- or eight-digit level. Tariff line data were matched to Standard International Trade Classification (SITC) revision 3 codes to define commodity groups and import weights. To the extent possible, specific rates have been converted to their ad valorem equivalent rates and have been included in the calculation of weighted mean tariffs. Import weights were calculated using the United Nations Statistics Division s Commodity Trade (Comtrade) database. Effectively applied tariff rates at the six- and eight-digit product level are averaged for products in each commodity group. When the effectively applied rate is unavailable, the most favored nation rate is used instead.')):
    return quotes.tariff_rates()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')

@app.get("/lia-defi/tourism_statistics")
async def read(q: Optional[str]=Query(None,description='International tourism receipts are expenditures by international inbound visitors, including payments to national carriers for international transport. These receipts include any other prepayment made for goods or services received in the destination country. They also may include receipts from same-day visitors, except when these are important enough to justify separate classification. For some countries they do not include receipts for passenger transport items. Data are in current U.S. dollars.')):
    return quotes.tourism_statistics()
    raise HTTPException(status_code=404,description='You exceeded your rate limit, upgrade your plan or contact us')



