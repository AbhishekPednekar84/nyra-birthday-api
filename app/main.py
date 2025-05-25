from fastapi import FastAPI
from .database.db import create_db_and_tables
from .routers import invite


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(invite.router)
# app.include_router(orders.router)
# app.include_router(order_window.router)
