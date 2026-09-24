import os

import redis
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from sqlalchemy import func, select

from db import Session
from models import GreetingLog

# ox injects REDIS_URL from the redis service; the fallback keeps local dev usable.
REDIS_URL = os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL)

app = FastAPI()


@app.get("/api/greeting")
def greeting():
    # Read at runtime: changing GREETING_TAG in the ox env editor applies on restart, no rebuild.
    line = f"hello world oxzoo-fastapi-react_{os.environ['GREETING_TAG']}"
    # Every hit is logged to postgres; /api/stats reports the running count.
    with Session() as session:
        session.add(GreetingLog(greeting=line))
        session.commit()
    return PlainTextResponse(line)


@app.get("/api/visits")
def visits():
    # INCR is atomic; the TTL is set on the first hit so the counter expires.
    count = redis_client.incr("oxzoo:visits")
    if count == 1:
        redis_client.expire("oxzoo:visits", 3600)
    return {"visits": count}


@app.get("/api/stats")
def stats():
    with Session() as session:
        count = session.scalar(select(func.count(GreetingLog.id)))
    return {"greetings_logged": count}


@app.get("/health")
def health():
    return PlainTextResponse("ok")
