from urllib.request import urlopen
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd

date = 202201
gu_code = 11305
service_key = '<<SERVICE_KEY>>'

url = f'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptRent?LAWD_CD={gu_code}&DEAL_YMD={date}&serviceKey={service_key}'

result = urlopen(url)
house = BeautifulSoup(result, 'lxml-xml')
te = house.find_all('item')

datas = []

for i in range(len(te)):
    deposit = te[i].보증금액.string.strip()
    rent_fee = te[i].월세금액.string.strip()
    built_yr = te[i].건축년도.string.strip()
    dong_name = te[i].법정동.string.strip()
    apt_name = te[i].아파트.string.strip()
    size = te[i].전용면적.string.strip()
    gu_code = te[i].지역코드.string.strip()
    
    data = [deposit, rent_fee, built_yr, dong_name, apt_name, size, gu_code]
    datas.append(data)

df = pd.DataFrame(datas, columns=['deposit', 'rent_fee', 'built_yr', 'dong_name', 'apt_name', 'size', 'gu_code'])

df['deposit'] = df['deposit'].replace(',', '').astype(int)
df['rent_fee'] = df['rent_fee'].astype(int)
df['built_yr'] = df['built_yr'].astype(int)
df['size'] = df['size'].astype(float)
df['gu_code'] = df['gu_code'].astype(int)

df.info()
df.to_csv("Apart.csv")
