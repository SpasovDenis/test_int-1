import mysql.connector
from mysql.connector import Error

def insert_data(data_list):
    try:
        cnx = mysql.connector.connect(user='denis', password='kali',
                                      host='localhost',
                                      database='test')
        if cnx.is_connected():
            cursor = cnx.cursor()
            # Обновите запрос на вставку для включения колонок addr и addr_ind
            insert_query = "INSERT INTO test1 (addr, addr_ind) VALUES (%s, %s);"
            cursor.executemany(insert_query, data_list)
            cnx.commit()
            print("Данные успешно добавлены")
    except Error as e:
        print(f"Ошибка: {e}")
    finally:
        if cnx.is_connected():
            cursor.close()
            cnx.close()

if __name__ == '__main__':
    # Генерация 1000 строк с числами от 1 до ...
    data = [(i, i) for i in range(1, 2000001)][:2000000]
    insert_data(data)
