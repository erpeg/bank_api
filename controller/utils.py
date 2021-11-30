import json
from collections import deque
import numpy as np
from typing import Dict
from sklearn.preprocessing import normalize
import requests
import asyncio


class Controller:
    def __init__(self) -> None:
        self.queue = deque([])
        self.accounts_split = {
            "account1": 100
        }
        self.accounts_split_norm = {
            "account1": 1
        }
        self.current_positions = {}
        self.poistion_url = "http://localhost:8002/position_send"

    def add_work(self, item: dict):
        self.queue.append(item)

    def normalize_dict(self, input_dictionary: Dict[str, int]) -> Dict[str, float]:
        """Normalizing input dictionary

        Args:
            input_dictionary (Dict[str, int]): dictionary to normalize

        Returns:
            (Dict[str, float]): Normalized dictionary
        """
        accounts_to_normalize = np.array(list(input_dictionary.items()), dtype=object)
        accounts_to_normalize[:, 1] = normalize(accounts_to_normalize[:, 1].reshape(1, accounts_to_normalize.shape[0]))
        return dict(accounts_to_normalize)

    def zip_dicts(self, *dcts):
        if not dcts:
            return
        for i in set(dcts[0]).intersection(*dcts[1:]):
            yield (i,) + tuple(d[i] for d in dcts)

    def select_account(self, new_stock_positions_normalized):
        differences = tuple(self.zip_dicts(self.accounts_split_norm, new_stock_positions_normalized))
        dict_of_diff = {account_difference[0]:account_difference[1]-account_difference[2] for account_difference in differences}
        select_acc = max(dict_of_diff, key=dict_of_diff.get)
        return select_acc

    def do_work(self):
        to_process = self.queue.popleft()
        stock = to_process["stock_ticker"]
        quantity = to_process["quantity"]

        if stock in self.current_positions.keys():
            # populating keys absent in dictionary of already bought stocks
            for acc_key in self.accounts_split.keys():
                if acc_key not in self.current_positions[stock].keys():
                    self.current_positions[stock][acc_key] = 0.0

            # getting tuple of two dicts:
            for single_stock in range(quantity):
                stock_positions = self.current_positions[stock]
                stock_positions_norm = self.normalize_dict(stock_positions)
                chosen_account = self.select_account(stock_positions_norm)
                self.current_positions[stock][chosen_account] += 1
            

        else:
            self.current_positions[stock] = {}
            # populating keys absent in dictionary of already bought stocks
            for acc_key in self.accounts_split.keys():
                if acc_key not in self.current_positions[stock].keys():
                    self.current_positions[stock][acc_key] = 0.0

            # getting tuple of two dicts:
            for single_stock in range(quantity):
                stock_positions = self.current_positions[stock]
                stock_positions_norm = self.normalize_dict(stock_positions)
                chosen_account = self.select_account(stock_positions_norm)
                self.current_positions[stock][chosen_account] += 1

    async def run_works(self):
        await asyncio.sleep(5.)
        while True:
            await asyncio.sleep(0.1)
            try:
                self.do_work()
            except IndexError:
                # waiting for tasks
                pass

    async def send_data(self):
        while True:
            requests.post(self.poistion_url, data=json.dumps(self.current_positions))
            await asyncio.sleep(7.95)