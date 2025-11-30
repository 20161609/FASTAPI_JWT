from __future__ import annotations

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.init import database, init_models
from app.route import auth, test

load_dotenv()

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://127.0.0.1:5500")

print("FRONTEND_ORIGIN:", FRONTEND_ORIGIN)

app = FastAPI(title="FastAPI Cookie JWT Auth")


@app.on_event("startup")
async def startup() -> None:
    print("Connecting to database and creating models...")
    init_models()
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    print("Disconnecting from database...")
    await database.disconnect()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(test.router, prefix="/test", tags=["test"])


@app.get("/")
async def root():
    return {"Welcome": "FastAPI server (JWT in HttpOnly cookies)"}
