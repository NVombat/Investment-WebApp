# Import Libraries and functions
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import stock

app = FastAPI()

@app.get('/buy')
def buy_stocks(date:str, stock_symbol: str, price: float, quantity: int, email: str,
               tablename: str='stock',path: str='app.db'):
    data = (date, stock_symbol, price, quantity, email)
    stock.buy(tablename, data, path=path)
