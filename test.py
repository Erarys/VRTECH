import psycopg2
from psycopg2 import OperationalError

DB_HOST = "localhost"
DB_PORT = 1234
DB_USER = "admin"
DB_PASS = "admin"
DB_NAME = "kaspi_db"

def test_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASS,
            dbname=DB_NAME,
            connect_timeout=5
        )
        print("✅ Успешное подключение к базе данных!")
        conn.close()
    except OperationalError as e:
        print("❌ Ошибка подключения:")
        print(e)

if __name__ == "__main__":
    test_connection()
