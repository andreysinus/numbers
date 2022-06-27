import os
import threading
import time
import httplib2
import urllib.request


from xml.dom import minidom
from datetime import date, datetime
from bdConfig import gSheet_id, table_name
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from bdConfig import delayUpdate



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
                    "Order" int,
                    "priceDollar" numeric,
                    "priceRub" numeric,
                    "deliveryDate" date
                );
                """
            )
            connection.commit()
            print("Table created")

def clearTable(connection):
    with connection.cursor() as cursor:
            cursor.execute(f"""
                DELETE FROM {table_name};
            """)
            connection.commit()
            print("Table cleared")
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
            
    return usdCurrency

def updateTable(res, connection):
    #Получение курса доллара
    usdCurrency = get_dollar()
    val = res.get('values', [])
    for rows in val:
        if rows!=[]:
            rubVal = float(rows[2])*usdCurrency
            rubVal=round(rubVal,2)
            checkDeliveryDate(rows[3],rows[0],rows[1])
            with connection.cursor() as cursor:
                cursor.execute(f"""
                INSERT INTO {table_name.lower()} VALUES ({rows[0]}, {rows[1]}, {rows[2]} ,{rubVal}, '{rows[3]}') 
                """)
            connection.commit()

def checkDeliveryDate(delDate, idOfDelivery, numOfDelivery):
    newDate=datetime.strptime(delDate,'%d.%m.%Y')
    nowDate=datetime.strptime(str(date.today()),'%Y-%m-%d')
    if newDate<nowDate:
        print("Срок поставки прошел у заказа с номером " + numOfDelivery+" (ID: "+idOfDelivery+"). Указанная дата поставки:"+ delDate)
        return


def getSheet(sheet, connection):
        #Получение таблицы из Google Sheets
        res = sheet.values().get(spreadsheetId=gSheet_id, range="Лист1!A2:D999").execute()

        #Очистка таблицы
        clearTable(connection)

        #Заполнение таблицы
        updateTable(res, connection)

        #Задержка между выполнением
        time.sleep(delayUpdate)

        #Повторный запуск функции
        threading.Timer(60.0, getSheet(sheet, connection)).start()