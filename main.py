from curses import reset_shell_mode
import os

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

def get_service():

    creds_json = os.path.dirname(__file__) + "/service.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)


#ID таблицы
gSheet_id= "1SpznG225ttDbGRtLA3abzAusSkx0peQZTtHTaMgFudE"
service = get_service()
sheet = service.spreadsheets()

res = sheet.values().batchGet(spreadsheetId=gSheet_id, ranges=["Лист1"]).execute()

print(res)