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
redisAddr = os.getenv('REDIS') 

if daskAddr == "" or redisAddr == "":
   print("DASK_SCHEDULER and REDIS_ADDR envvars must not be empty")
   os.exit(1)

# TODO: error handling would be best
rArr = redisAddr.split(":")
if len(rArr) != 2:
   print("REDIS_ADDR must contain URI and Port separated by ':'")
   os.exit(2)

# Initialize Dask and Redis clients
client = Client(daskAddr)
client.upload_file('nano.py')
r = redis.Redis(host=rArr[0], port=rArr[1], decode_responses=True)


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
