import utils
import multiprocessing as mp

max_number_of_accounts = 10
aum_url = "http://localhost:8000/aum"

if __name__ == '__main__':
    utils.send_request(aum_url, max_number_of_accounts)
