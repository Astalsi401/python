from msilib.schema import tables
from unittest import result
import requests
import os
import sys
sys.path.append('D:/Documents/python/myFunction')
from myfuc import readCsv
from bs4 import BeautifulSoup as bs

pwd = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')


url = 'https://pmds.fda.gov.tw/illegalad/CaseSearch.aspx'
session = requests.session()
res = session.get(url)

soup = bs(res.text, 'lxml')
view_state = soup.find(id='__VIEWSTATE')['value']
view_state_generator = soup.find(id='__VIEWSTATEGENERATOR')['value']
previous_page = soup.find(id='__PREVIOUSPAGE')['value']
event_validation = soup.find(id='__EVENTVALIDATION')['value']

header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Length': '8702',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'ASP.NET_SessionId=fiogcmldyrdk5dviq2ywsxet; cookiesession1=678A3E25CE6F1D4C863228AAEC743F8B; _gcl_au=1.1.287931125.1652236651; _gid=GA1.3.899801686.1652236652; _ga=GA1.3.2023565515.1652236651; _ga_8CBFE781ED=GS1.1.1652236651.1.1.1652236803.0',
    'Host': 'pmds.fda.gov.tw',
    'Origin': 'https://pmds.fda.gov.tw',
    'Referer': url,
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
}

payload = {
    '__VIEWSTATE': view_state,
    '__VIEWSTATEGENERATOR': view_state_generator,
    '__PREVIOUSPAGE': previous_page,
    '__EVENTVALIDATION': event_validation,
    'ctl00$txtSearchValue': '台塑生醫',
    'ctl00$btnAdvanceSearch': '進階查詢',
    'ctl00$RepeaterHotKeywords$ctl00$hdnKeyword': '保健食品',
    'ctl00$RepeaterHotKeywords$ctl01$hdnKeyword': '益生菌',
    'ctl00$RepeaterHotKeywords$ctl02$hdnKeyword': '食品',
    'ctl00$RepeaterHotKeywords$ctl03$hdnKeyword': '艾多美',
    'ctl00$RepeaterHotKeywords$ctl04$hdnKeyword': '安麗',
    'ctl00$RepeaterHotKeywords$ctl05$hdnKeyword': '鴕鳥精',
    'ctl00$RepeaterHotKeywords$ctl06$hdnKeyword': '橙姑娘',
    'ctl00$RepeaterHotKeywords$ctl07$hdnKeyword': '婕樂纖',
    'ctl00$RepeaterHotKeywords$ctl08$hdnKeyword': '玫琳凱',
    'ctl00$RepeaterHotKeywords$ctl09$hdnKeyword': '可妮絲',
    'ctl00$Content$lvList$ctrl0$hdnType': 'New',
    'ctl00$Content$lvList$ctrl0$hdnCaseId': '102-N00190',
    'ctl00$Content$lvList$ctrl1$hdnType': 'New',
    'ctl00$Content$lvList$ctrl1$hdnCaseId': '102-N01702',
    'ctl00$Content$lvList$ctrl2$hdnType': 'New',
    'ctl00$Content$lvList$ctrl2$hdnCaseId': '102P0349',
    'ctl00$Content$lvList$ctrl3$hdnType': 'New',
    'ctl00$Content$lvList$ctrl3$hdnCaseId': '102TA0070',
    'ctl00$Content$lvList$ctrl4$hdnType': 'New',
    'ctl00$Content$lvList$ctrl4$hdnCaseId': '102TP0057',
    'ctl00$Content$lvList$ctrl5$hdnType': 'New',
    'ctl00$Content$lvList$ctrl5$hdnCaseId': '102TP0202',
    'ctl00$Content$lvList$ctrl6$hdnType': 'New',
    'ctl00$Content$lvList$ctrl6$hdnCaseId': '102TP0771',
    'ctl00$Content$lvList$ctrl7$hdnType': 'New',
    'ctl00$Content$lvList$ctrl7$hdnCaseId': '102TP1068',
    'ctl00$Content$lvList$ctrl8$hdnType': 'New',
    'ctl00$Content$lvList$ctrl8$hdnCaseId': '102TP1115',
    'ctl00$Content$lvList$ctrl9$hdnType': 'New',
    'ctl00$Content$lvList$ctrl9$hdnCaseId': '102TP1391',
}
res = session.post(url, data=payload, headers=header)

print(res.text)
