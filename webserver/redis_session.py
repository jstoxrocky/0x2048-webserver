from redis import Redis
import os


REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']


def get_session():
    return Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
