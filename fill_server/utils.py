import random
import json as simplejson
import requests
import time
from datetime import datetime

# Setting up possible stocks
stock_ticker_tuple = ("AXA", "SAM", "TES", "LAS", "DAS", "KAS", "PON", "DIR", "ETQ", "OLO")

def generate_fill():
    """Generating random values of trade fills

    Returns:
        str: JSON with randomly generated trade fills
    """
    fill_data = {}
    fill_data["stock_ticker"] = random.choice(stock_ticker_tuple)
    fill_data["price"] = random.randint(1, 100)
    fill_data["quantity"] = random.randint(1, 100)
    return simplejson.dumps(fill_data)

def send_request(fill_endpoint):
    """Sending request with randomly generated trade fills

    Args:
        fill_endpoint (str): URL to fill endpoint
    """
    while True:
        data_to_send = generate_fill()  # generating data
        response = requests.post(fill_endpoint, data=data_to_send)
        print(f"Sent {data_to_send} on {datetime.now()}.")
        time.sleep(random.uniform(0.0, 10.0))





