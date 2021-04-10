#Import Libraries and functions
from fastapi import FastAPI 
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from models import stock


import sqlite3


app = FastAPI()

@app.get('/buy')
async def buy(user : str):
    
    response = RedirectResponse(url='http://localhost:8000/trade')
    
    return response

@app.get('/sell')
async def sell(user : str):
    
    response = RedirectResponse(url='http://localhost:8000/trade')
    
    return response