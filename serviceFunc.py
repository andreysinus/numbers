import os
import threading
from xml.dom import minidom
import httplib2
import urllib.request
from pprint import pprint

from bdConfig import gSheet_id
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import urllib3


table_name="TestTable"
cbrfURL="https://www.cbr.ru/scripts/XML_daily.asp?"


def get_service_sacc():

    creds_json = os.path.dirname(__file__) + "/service.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)

def createTable(connection):
     with connection.cursor() as cursor:
            cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS {table_name}
                (
                    id serial,
                    "priceDollar" numeric,
                    "priceRub" numeric,
                    "deliveryDate" date
                );
                """
            )
            connection.commit()
            print("Table created")

def clearTable(connection):
    

def get_data(CBRFurl):
    web_file=urllib.request.urlopen(CBRFurl)
    return web_file.read()


def get_dollar():
    xmlCont=get_data(cbrfURL)
    dom=minidom.parseString(xmlCont)
    dom.normalize()

    elements = dom.getElementsByTagName("Valute")
    CHcode=""
    usdCurrency=0
    for node in elements:
        for child in node.childNodes:
            if child.nodeType ==1:
                if child.tagName=="CharCode":
                    if child.firstChild.nodeType == 3:
                        CHcode = child.firstChild.data
                if child.tagName=="Value":
                    if child.firstChild.nodeType == 3:
                        usdValue=float(child.firstChild.data.replace(',','.'))
            if CHcode=="USD":
                usdCurrency=usdValue
            
    #print(usdCurrency)
    return usdCurrency

def getSheet(sheet):
    res = sheet.values().get(spreadsheetId=gSheet_id, range="Лист1!A1:D999").execute()
    threading.Timer(5.0, getSheet).start()