

import redis
import json

r = redis.Redis(
  host='redis-12044.c330.asia-south1-1.gce.redns.redis-cloud.com',
  port=12044,
  password='CApgs4cIuoDFAV0EnQ9wXCmMwsZYY4Sq')
# Kiểm tra kết nối
try:
    r.ping()
    print("Connected to Redis")
except redis.ConnectionError:
    print("Could not connect to Redis")

def get_human_chat():
    r.flushall()

    keys = r.keys('*')
    print(len(keys))
    newest_key = keys[len(keys)-1]

    key_str = newest_key.decode('utf-8')
    key_type = r.type(key_str).decode('utf-8')

    if key_type == 'string':
        value = r.get(key_str).decode('utf-8')
    elif key_type == 'list':
        value = [item.decode('utf-8') for item in r.lrange(key_str, 0, -1)]
    elif key_type == 'set':
        value = [item.decode('utf-8') for item in r.smembers(key_str)]
    elif key_type == 'hash':
        value = {k.decode('utf-8'): v.decode('utf-8') for k, v in r.hgetall(key_str).items()}
    else:
        value = "Unsupported key type"

    human_chat = value[1]
    print("human_chat",human_chat)
    human_chat_obj = json.loads(human_chat)

    human_chat_content = human_chat_obj['data']['content']
    return human_chat_content

