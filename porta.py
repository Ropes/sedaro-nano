import os
import json
from functools import reduce
from operator import __or__
from random import random
from nano import propagate_reps, QRangeStore
import redis

import dask
from dask.distributed import Client
from flask import Flask
 
# Remove 1st argument from the
# list of command line arguments
daskAddr = os.getenv('DASK_SCHEDULER')
redisAddr = os.getenv('REDIS_ADDR') 

# Initialize Dask and Redis clients
client = Client(daskAddr)
client.upload_file('nano.py')
r = redis.Redis(host=redisAddr, port=6379, decode_responses=True)


app = Flask(__name__)

@app.route("/")
def hello_world():
    return '<p>Hello, World!</p>'

# App route /<propagation count>
@app.route('/propagate/<int:n>')
def prop_route(n):
  # Lookup Redis for data
  data = r.hgetall('propagated[{n}]')
  if data:
    # render html page and return
    print('data returned: {data}')
    return '<p>propagation</p>'

  # If no data, propagate(n)
  store = propagate_reps(client, n)
  d = f"data = {json.dumps(store.store, indent=3)}"
  # store data to Redis
  r.hset('propagated[{n}]', key='propagated[{n}]', value=d)
  return '<p>launched propagation!</p>'
