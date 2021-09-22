from back import get_current_stock_price
from models.users import hash_pwd


class Base:
    def __init__(self) -> None:
        self.contact_us_data = {
            "path": "app.db",
            "message": "test message",
            "email": "ronaldo72emiway@gmail.com",
        }

        self.stock_data = {
            "path": "app.db",
            "tablename": "stock",
            "email": "ronaldo72emiway@gmail.com",
            "stock_symbol": "AAPL",
            "quantity": 1,
            "price": get_current_stock_price("AAPL"),
            "date": "19-09-2021",
        }

        self.user_data = {
            "path": "app.db",
            "tablename": "user",
            "email": "ronaldo72emiway@gmail.com",
            "name": "Nikhill Vombatkere",
            "password": hash_pwd("abc123ABC"),
            "code": 0,
        }

        self.test_data = {
            "path": "test.db",
            "message": "test message",
            "email": "test@gmail.com",
            "name": "Test User",
            "password": hash_pwd("test123"),
            "tablename": "stock",
            "stock_symbol": "AAPL",
            "quantity": 1,
            "price": get_current_stock_price("AAPL"),
            "date": "19-09-2021",
        }
