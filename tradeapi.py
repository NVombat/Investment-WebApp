# Import Libraries and functions
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from models import stock

app = FastAPI()

"""
For buying:
On clicking the buy button the transaction is carried out and the stock table is updated using the buy function
This inserts data into the table for a particular user
Page is then redirected back to the trade page
"""
@app.get('/buy')
async def buy_stocks(date:str, stock_symbol: str, price: float, quantity: int, email: str,
               tablename: str='stock',path: str='app.db'):
    data = (date, stock_symbol, price, quantity, email)
    stock.buy(tablename, data, path=path)

    response = RedirectResponse(url='http://localhost:8000/trade')
    
    return response


"""
For Selling:
On clicking the sell button the transaction is carried out and the stock table is updated using the sell function
This deletes data from the table for a particular user
Page is then redirected back to the trade page
"""
@app.get('/sell')
async def sell_stocks(stock_symbol: str, quantity: int, email: str,
               tablename: str='stock',path: str='app.db'):
    data = (stock_symbol, quantity, email)
    stock.sell(tablename, data, path=path)
    
    response = RedirectResponse(url='http://localhost:8000/trade')
    
    return response

#COMMAND TO RUN FASTAPI
#uvicorn tradeapi:app --reload --port 1212