import pytest
import mysql.connector
from datetime import datetime

# Фикстура для подключения к базе данных
@pytest.fixture(scope='module')
def db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='test',
        user='denis',
        password='kali'
    )
    yield connection
    connection.close()

# Функция для выполнения запроса и измерения времени его выполнения
def execute_query(connection, query):
    with connection.cursor() as cursor:
        start_time = datetime.now()
        cursor.execute(query)
        results = cursor.fetchall()
        duration = (datetime.now() - start_time).total_seconds()
    return results, duration

# Функциональный тест (для примера оставлено select ... like '%1%')
def test_functional_select_like(db_connection):
    no_index_results, _ = execute_query(db_connection, "SELECT col FROM example_table WHERE col LIKE '%1%';")
    print('\nВывод запроса SELECT для столбца без индекса:', no_index_results)
    index_results, _ = execute_query(db_connection, "SELECT col_ind FROM example_table WHERE col_ind LIKE '%1%';")
    print('Вывод запроса SELECT для столбца с индексом:',index_results)
    assert no_index_results == index_results, "Результаты запросов должны совпадать"

# Перфоманс тест (для примера оставлено select ... like '%1234')
def test_performance_select_like(db_connection):
    _, no_index_duration = execute_query(db_connection, "SELECT addr FROM test1 WHERE addr LIKE '%1234';")
    print('\nВремя запроса SELECT для столбца без индекса:',no_index_duration)
    _, index_duration = execute_query(db_connection, "SELECT addr_ind FROM test1 WHERE addr_ind LIKE '%1234';")
    print( 'Время запроса SELECT для столбца с индексом:' ,index_duration)
    print('Разница времени:', no_index_duration - index_duration)
    assert no_index_duration >= index_duration, "Время выполнения запроса с индексом должно быть меньше или равно времени без индекса"
