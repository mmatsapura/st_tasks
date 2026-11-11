import os
import psycopg2
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()
load_dotenv()
db_name = os.getenv('DBNAME')
db_user = os.getenv('USER')
db_password = os.getenv('PASSWORD')
db_host = os.getenv('HOST')


@app.get('/users')
async def get_users() -> list:
    conn = psycopg2.connect(dbname=db_name, user=db_user,
                            password=db_password, host=db_host)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_data')
    records = cursor.fetchall()

    cursor.close()
    conn.close()
    return records


@app.post('/create_user')
async def create_user(name: str, age: int) -> dict:
    conn = psycopg2.connect(dbname=db_name, user=db_user,
                            password=db_password, host=db_host)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_data (name, age) VALUES (%s, %s);', (name, age))
    conn.commit()

    cursor.close()
    conn.close()
    return {'Name': name, 'Age': age, 'message': 'Успешно добавлено в БД'}