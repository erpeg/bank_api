import random
import simplejson
import requests
import time

stock_ticker_tuple = ("AXA", "SAM", "TES", "LAS", "DAS", "KAS", "PON", "DIR", "ETQ", "OLO")

def generate_aum_data():
    aum_data = {}
    aum_data["stock_ticker"] = random.choice(stock_ticker_tuple)
    aum_data["price"] = random.randint(1, 100)
    aum_data["quantity"] = random.randint(1, 100)
    return simplejson.dumps(aum_data)

def send_request():
    server_url = "http://localhost:8000/aum"
    while True:
        response = requests.post(server_url, data=generate_aum_data())
        time.sleep(random.uniform(0.0, 10.0))





