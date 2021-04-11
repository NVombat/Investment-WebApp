# Import Libraries and functions
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import stock

app = FastAPI()

@app.get('/buy')
async def buy_stocks(date:str, stock_symbol: str, price: float, quantity: int, email: str,
               tablename: str='stock',path: str='app.db'):
    data = (date, stock_symbol, price, quantity, email)
    stock.buy(tablename, data, path=path)

    response = RedirectResponse(url='http://localhost:8000/trade')
    
    return response

@app.get('/sell')
async def sell_stocks(stock_symbol: str, quantity: int, email: str,
               tablename: str='stock',path: str='app.db'):
    data = (stock_symbol, quantity, email)
    stock.sell(tablename, data, path=path)
    
    response = RedirectResponse(url='http://localhost:8000/trade')
    
    return response
