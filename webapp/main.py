from fastapi import FastAPI
import os
import redis

app = FastAPI()
redis_host = os.getenv('REDIS_HOST', 'redis_connect')

try:
    r = redis.Redis(host=redis_host, port=6379, decode_responses=True)
    r.ping()
    redis_available = True
except Exception:
    redis_available = False

file = '/webapp/data/visits.txt'


def count_visits():
    os.makedirs(os.path.dirname(file), exist_ok=True)
    try:
        with open(file, 'r+', encoding='utf_8') as f:
            f.seek(0)
            content = f.read().strip()
            count = int(content)
            count += 1
            f.seek(0)
            f.write(str(count))
            return count
    except FileNotFoundError:
        count = 0
        with open(file, 'w', encoding='utf-8') as f:
            f.write(str(count + 1))
        return count + 1


@app.get('/')
def home():
    r_count = "Redis недоступен"
    if redis_available:
        r.incr("redis_counter")
        r_count = r.get('redis_counter')
    file_count = count_visits()
    return {
        "file_count": file_count,
        "redis_count": r_count
    }