import os
import psycopg2
from fastapi import FastAPI

app = FastAPI()

db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')


@app.get('/users')
def get_users() -> list:
    conn = psycopg2.connect(dbname=db_name, user=db_user,
                            password=db_password, host=db_host)
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user_data')
        records = cursor.fetchall()
        return records
    finally:
        if cursor:
            cursor.close()
        conn.close()



@app.post('/create_user')
def create_user(name: str, age: int) -> dict:
    conn = psycopg2.connect(dbname=db_name, user=db_user,
                            password=db_password, host=db_host)
    cursor = None
    try:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user_data (name, age) VALUES (%s, %s);', (name, age))
        conn.commit()
        return {'Name': name, 'Age': age, 'message': 'Успешно добавлено в БД'}
    finally:
        if cursor:
            cursor.close()
        conn.close()
