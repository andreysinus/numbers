import os
import psycopg2


from bdConfig import host,user, password,db_name, gSheet_id
from serviceFunc import get_service_sacc, createTable

def main():
    #try: 
        service = get_service_sacc()
        sheet = service.spreadsheets()
        res = sheet.values().get(spreadsheetId=gSheet_id, range="Лист1!A1:D999").execute()
        print(res)
        
        connection=psycopg2.connect(
                user=user,
                host=host,
                password=password,
                database=db_name
            )
        createTable(connection)
       
    #except:
        #print("Error while connection with PostgreSQL")
    #finally:
        #if connection:
            #connection.close()
            #print("PostgreSQL connection closed")


if __name__ == '__main__':
   main()