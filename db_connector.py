import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            username='root',
            password='',
            database='db_ApiTelegram'
        )
        if connection.is_connected():
            print('Connected to MySQL database')
            return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS inbox (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       username VARCHAR(255) NOT NULL,
                       message TEXT NOT NULL,
                       date TIMESTAMP NOT NULL
                       )
                    """)
        cursor.execute("""CREATE TABLE IF NOT EXISTS outbox (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       username VARCHAR(255) NOT NULL,
                       message TEXT NOT NULL,
                       date TIMESTAMP NOT NULL
                       )
                    """)
        print('Tables created successfully')
    except Error as e:
        print(f"Error creating tables: {e}")

def main():
    connection = create_connection()
    if connection:
        create_tables(connection)
        connection.close()
        print('Connection closed')

if __name__ == "__main__":
    main()
