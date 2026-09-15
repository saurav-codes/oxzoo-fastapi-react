import os

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.get("/api/greeting")
def greeting():
    # Read at runtime: changing GREETING_TAG in the ox env editor applies on restart, no rebuild.
    return PlainTextResponse(f"hello world oxzoo-fastapi-react_{os.environ['GREETING_TAG']}")


@app.get("/health")
def health():
    return PlainTextResponse("ok")
