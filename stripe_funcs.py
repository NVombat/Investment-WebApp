from dotenv import load_dotenv
import stripe
import os

from stripe.api_resources import price

load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_prod(prod_name: str):
    stripe.Product.create(
        name = prod_name
    ) 

def get_prod(prod_id: str):
    stripe.Product.retrieve(
        prod_id
    )

def create_price(prod_id: str, price_val: float):
    stripe.Price.create(
        unit_amount = price_val,
        currency = "inr",
        product = prod_id,
    )

def get_price(price_id: str):
    stripe.Price.retrieve(
        price_id,
    )