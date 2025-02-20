from flask import jsonify, make_response
import requests
from datetime import datetime
from abc import ABCMeta, abstractmethod

class GenericSource(metaclass=ABCMeta):
    
    def __init__(self,url,source_name):
        self.template_url = url
        self.source_name = source_name

    def get_source_name(self):
        return self.source_name

    @abstractmethod
    def get_prices(self,currency_pairs):
        full_response = {}
        full_response[self.source_name] = {}
        for currency_pair in currency_pairs.split(","):
            from_currency = currency_pair.split("_")[0]
            to_currency = currency_pair.split("_")[1]
            url = self.template_url.replace("FROM_CURRENCY",from_currency).replace("TO_CURRENCY",to_currency)
            
            response = requests.get(url).json()
            current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_response[self.source_name][currency_pair] = {"processed_at":current_timestamp,"source":self.source_name, "payload":response}
        return full_response
        
