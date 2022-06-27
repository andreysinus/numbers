import psycopg2
import time

from bdConfig import host,user, password,db_name
from serviceFunc import get_service_sacc, createTable, getSheet
connection=""
x=True
def main():
    try:
        #Подключение к таблице
        service = get_service_sacc()
        sheet = service.spreadsheets()
        
        #Подключение к БД
        connection=psycopg2.connect(
                user=user,
                host=host,
                password=password,
                database=db_name
            )
        #Создание таблицы, при её отсутсвии
        createTable(connection)
        #Внесение изменений в БД
        getSheet(sheet, connection)
            
    except:
        print("Error when working with the table")
    finally:
        if connection:
            connection.close()
            print("PostgreSQL connection closed")
    
if __name__ == '__main__':
   main()