import os
import logging
from typing import Union

import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

@app.get("/")
def read_root():
    if not DATABASE_URL:
        raise HTTPException(status_code=500, detail="DATABASE_URL is not set")

    try:
        with psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
            connect_timeout=5,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM experience LIMIT 100;")
                rows = cur.fetchall()
    except psycopg.Error as exc:
        logging.exception("Database connection failed: %s", exc)
        raise HTTPException(status_code=500, detail="Database connection failed")

    return {"experience": rows}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}