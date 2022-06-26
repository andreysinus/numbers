import os

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

def get_service_sacc():

    creds_json = os.path.dirname(__file__) + "/service.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


#ID таблицы
gSheet_id= "1SpznG225ttDbGRtLA3abzAusSkx0peQZTtHTaMgFudE"

#service = get_service_simple()
service = get_service_sacc()
sheet = service.spreadsheets()

res = sheet.values().get(spreadsheetId=gSheet_id, range="Лист1!A1:A999").execute()

print(res)