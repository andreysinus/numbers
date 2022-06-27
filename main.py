import psycopg2
import time

from bdConfig import host,user, password,db_name, gSheet_id
from serviceFunc import get_dollar, get_service_sacc, createTable
usdCurrency=0
x=True
def main():
    try: 
        service = get_service_sacc()
        sheet = service.spreadsheets()
        

        connection=psycopg2.connect(
                user=user,
                host=host,
                password=password,
                database=db_name
            )
        createTable(connection)
        while x==True:
            
            time.sleep(60)
            
    except:
        print("Error while connection with PostgreSQL")
    finally:
        if connection:
            connection.close()
            print("PostgreSQL connection closed")

if __name__ == '__main__':
   main()