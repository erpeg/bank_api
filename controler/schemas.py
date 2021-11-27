from fastapi import FastAPI
from pydantic import BaseModel


class Accounts(BaseModel):
    stock_ticker: str
    price: int
    quantity: float

