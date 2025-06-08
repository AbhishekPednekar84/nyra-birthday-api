from fastapi import FastAPI
from .database.db import create_db_and_tables
from .routers import invite
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://api.nyrasbirthday.xyz",
    ],  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(invite.router)
# app.include_router(orders.router)
# app.include_router(order_window.router)
