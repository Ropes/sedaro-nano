FROM scratch 
## TODO: Fix image base

ENV DASK_SCHEDULER localhost:8786
ENV REDIS_URL localhost:6379

WORKDIR /tmp
ADD requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt


RUN mkdir /sedaro
ADD nano.py      /sedaro/
ADD porta.py     /sedaro/
ADD index.html   /sedaro/

# TODO: exec flask
ENTRYPOINT [ "flask", "--app", "porta", "run" ]