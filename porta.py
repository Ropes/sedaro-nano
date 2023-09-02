import os
import json
from functools import reduce
from operator import __or__
from random import random
from nano import propagate_reps, QRangeStore
import redis

import dask
from dask.distributed import Client
from flask import Flask, render_template
 
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
  json_data = r.get(f'propagated[{n}]')
  if json_data:
    data = json.loads(json_data) 
    # render html page and return
    #print(f'cache data returned: {data}')
    return render_template('index.html', data=data)

  # If no data, propagate(n)
  store = propagate_reps(client, n)
  d = json.dumps(store.store)
  # store data to Redis
  r.set(f'propagated[{n}]', d)

  # return template
  return render_template('index.html', data=d)
