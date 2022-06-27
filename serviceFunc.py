import os
import httplib2
import psycopg2

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

table_name="TestTable"

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
