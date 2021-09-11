from dotenv import load_dotenv
import stripe
import os

load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_prod(prod_name: str):
    stripe.Product.create(
        name = prod_name
    ) 

def get_prod(prod_id: str):
    prod_obj = stripe.Product.retrieve(
        prod_id
    )
    return prod_obj

def create_price(prod_id: str, price_val: float):
    stripe.Price.create(
        unit_amount = price_val,
        currency = "inr",
        product = prod_id,
    )

def get_full_price_info(price_id: str):
    price_obj = stripe.Price.retrieve(
        price_id,
    )
    return price_obj

def get_price_value(price_id: str):
    price_obj = get_full_price_info(price_id)
    price_val = price_obj['unit_amount']/100
    return price_val