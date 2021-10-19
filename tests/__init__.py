"""
Test folder for all
integration tests
"""

from back import get_current_stock_price


class Base:
    def __init__(self) -> None:
        test_price = float(get_current_stock_price("AAPL"))

        self.stock_data = {
            "path": "app.db",
            "tablename": "stock",
            "email": "ronaldo72emiway@gmail.com",
            "stock_symbol": "AAPL",
            "quantity": 1,
            "price": test_price,
            "date": "19-09-2021",
        }
